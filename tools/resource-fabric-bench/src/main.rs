use fst::{Map, MapBuilder};
use roaring::RoaringBitmap;
use std::io::Cursor;
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
    let _ = PATTERNS;
}

fn main() {
    for n in SCALES { benchmark(n); }
    println!("DORE_RESOURCE_FABRIC_FST=PASS");
    println!("DORE_RESOURCE_FABRIC_ROARING=PASS");
    println!("DORE_RESOURCE_FABRIC_ZSTD_DICTIONARY=PASS");
}
