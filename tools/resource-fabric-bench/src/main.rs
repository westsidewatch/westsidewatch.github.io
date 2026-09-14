use arrow_array::{ArrayRef, RecordBatch, StringArray, UInt64Array, UInt8Array};
use bytes::Bytes;
use fst::{Map, MapBuilder};
use parquet::arrow::arrow_reader::ParquetRecordBatchReaderBuilder;
use parquet::arrow::{ArrowWriter, ProjectionMask};
use roaring::RoaringBitmap;
use std::io::Cursor;
use std::sync::Arc;
use std::time::Instant;

const SCALES: [usize; 3] = [10_000, 100_000, 1_000_000];
const PATTERNS: [(&str, &str, &str, &str); 4] = [
    ("en", "book", "public-domain", "remote"),
    ("zh", "book", "link-only", "remote"),
    ("en", "pdf", "link-only", "remote"),
    ("zh", "video", "link-only", "browser-runtime"),
];

fn key(i: usize) -> String { format!("Work {i:07}") }
fn delta(i: usize) -> Vec<u8> {
    format!("{i}|{}|Work {i:07}|Creator {:04}|src:{i:07x}\n", i % 4, i % 4096).into_bytes()
}

fn batch(start: usize, end: usize) -> RecordBatch {
    let ids: Vec<u64> = (start..end).map(|i| i as u64).collect();
    let titles: Vec<String> = (start..end).map(key).collect();
    let creators: Vec<String> = (start..end).map(|i| format!("Creator {:04}", i % 4096)).collect();
    let patterns: Vec<u8> = (start..end).map(|i| (i % 4) as u8).collect();
    let pointers: Vec<String> = (start..end).map(|i| format!("src:{i:07x}")).collect();
    let languages: Vec<&str> = (start..end).map(|i| PATTERNS[i % 4].0).collect();
    let kinds: Vec<&str> = (start..end).map(|i| PATTERNS[i % 4].1).collect();
    let rights: Vec<&str> = (start..end).map(|i| PATTERNS[i % 4].2).collect();
    let access: Vec<&str> = (start..end).map(|i| PATTERNS[i % 4].3).collect();

    let cols: Vec<(&str, ArrayRef)> = vec![
        ("id", Arc::new(UInt64Array::from(ids))),
        ("title", Arc::new(StringArray::from(titles))),
        ("creator", Arc::new(StringArray::from(creators))),
        ("pattern", Arc::new(UInt8Array::from(patterns))),
        ("pointer", Arc::new(StringArray::from(pointers))),
        ("language", Arc::new(StringArray::from(languages))),
        ("kind", Arc::new(StringArray::from(kinds))),
        ("rights", Arc::new(StringArray::from(rights))),
        ("access", Arc::new(StringArray::from(access))),
    ];
    RecordBatch::try_from_iter(cols).expect("record batch")
}

fn parquet_projection_benchmark(n: usize) {
    let start = Instant::now();
    let mut parquet_bytes = Vec::new();
    {
        let first = batch(0, n.min(65_536));
        let schema = first.schema();
        let mut writer = ArrowWriter::try_new(&mut parquet_bytes, schema, None).expect("parquet writer");
        writer.write(&first).expect("write first batch");
        let mut offset = first.num_rows();
        while offset < n {
            let end = (offset + 65_536).min(n);
            writer.write(&batch(offset, end)).expect("write parquet batch");
            offset = end;
        }
        writer.close().expect("close parquet writer");
    }
    let build_ms = start.elapsed().as_secs_f64() * 1000.0;

    let bytes = Bytes::from(parquet_bytes);
    let builder = ParquetRecordBatchReaderBuilder::try_new(bytes.clone()).expect("parquet reader builder");
    let projected_cols = [0usize, 1, 2];
    let mut projected_physical_bytes = 0usize;
    for row_group in builder.metadata().row_groups() {
        for &idx in &projected_cols {
            projected_physical_bytes += row_group.column(idx).compressed_size() as usize;
        }
    }
    let mask = ProjectionMask::leaves(builder.parquet_schema(), projected_cols);
    let read_start = Instant::now();
    let mut reader = builder
        .with_projection(mask)
        .with_batch_size(16_384)
        .build()
        .expect("projected parquet reader");
    let mut rows = 0usize;
    while let Some(item) = reader.next() {
        let projected = item.expect("projected record batch");
        assert_eq!(projected.num_columns(), 3);
        rows += projected.num_rows();
    }
    let read_ms = read_start.elapsed().as_secs_f64() * 1000.0;
    assert_eq!(rows, n);

    let total = bytes.len();
    let ratio = projected_physical_bytes as f64 / total as f64;
    println!(
        "works={n} parquet_total_bpw={:.6} surface_projection_bpw={:.6} surface_projection_ratio={:.6} parquet_build_ms={:.3} projected_read_ms={:.3}",
        total as f64 / n as f64,
        projected_physical_bytes as f64 / n as f64,
        ratio,
        build_ms,
        read_ms,
    );
    assert!(ratio < 0.75, "surface projection must avoid most canonical columns");
}

fn benchmark(n: usize) {
    let start = Instant::now();

    let mut fst_bytes = Vec::new();
    {
        let mut builder = MapBuilder::new(&mut fst_bytes).expect("fst builder");
        for i in 0..n {
            builder.insert(key(i), i as u64).expect("ordered fst insert");
        }
        builder.finish().expect("fst finish");
    }
    let fst = Map::new(fst_bytes.clone()).expect("fst map");

    let mut memberships = [RoaringBitmap::new(), RoaringBitmap::new(), RoaringBitmap::new(), RoaringBitmap::new()];
    let mut roaring_bytes = 0usize;
    for i in 0..n {
        memberships[i % 4].insert(i as u32);
    }
    for bitmap in &memberships {
        roaring_bytes += bitmap.serialized_size();
    }

    let sample_count = n.min(8192);
    let samples: Vec<Vec<u8>> = (0..sample_count).map(delta).collect();
    let sample_refs: Vec<&[u8]> = samples.iter().map(Vec::as_slice).collect();
    let dict = zstd::dict::from_samples(&sample_refs, 8192).expect("zstd dictionary train");

    let mut plain = Vec::new();
    for i in 0..n { plain.extend_from_slice(&delta(i)); }
    let compressed = zstd::stream::encode_all(Cursor::new(&plain), 6).expect("zstd encode");

    let mut encoder = zstd::stream::Encoder::with_dictionary(Vec::new(), 6, &dict).expect("zstd dict encoder");
    std::io::copy(&mut Cursor::new(&plain), &mut encoder).expect("zstd dict copy");
    let dict_compressed = encoder.finish().expect("zstd dict finish");

    let q0 = Instant::now();
    let mut checksum = 0u64;
    for j in 0..1000usize {
        let i = (j * 104729) % n;
        checksum ^= fst.get(key(i)).expect("fst lookup");
        checksum ^= memberships[i % 4].contains(i as u32) as u64;
    }
    let lookup_ms = q0.elapsed().as_secs_f64() * 1000.0;

    let total_compact = fst_bytes.len() + roaring_bytes + dict.len() + dict_compressed.len();
    println!(
        "works={n} fst_bpw={:.6} roaring_bpw={:.6} zstd_bpw={:.6} zstd_dict_bpw={:.6} compact_total_bpw={:.6} lookup1000_ms={:.6} build_ms={:.3} checksum={checksum}",
        fst_bytes.len() as f64 / n as f64,
        roaring_bytes as f64 / n as f64,
        compressed.len() as f64 / n as f64,
        dict_compressed.len() as f64 / n as f64,
        total_compact as f64 / n as f64,
        lookup_ms,
        start.elapsed().as_secs_f64() * 1000.0,
    );

    assert_eq!(fst.len(), n);
    assert_eq!(memberships.iter().map(|b| b.len()).sum::<u64>(), n as u64);
    assert!(fst.get(key(n - 1)).is_some());
    parquet_projection_benchmark(n);
}

fn main() {
    for n in SCALES { benchmark(n); }
    println!("DORE_RESOURCE_FABRIC_FST=PASS");
    println!("DORE_RESOURCE_FABRIC_ROARING=PASS");
    println!("DORE_RESOURCE_FABRIC_ZSTD_DICTIONARY=PASS");
    println!("DORE_RESOURCE_FABRIC_COLUMNAR_PROJECTION=PASS");
}
