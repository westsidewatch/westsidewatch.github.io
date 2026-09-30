"""Project Gutenberg -> DawnPublication adapter.

The adapter emits normalized publication metadata/resources. It does not fetch
or parse Gutenberg HTML itself; retrieval remains behind the lawful
materialization boundary.
"""
from __future__ import annotations

from dataclasses import dataclass

from dore_core.language.source_mapping import SourceMapping, map_public_domain_source
from dore_core.publication import DawnPublication, PublicationLink


@dataclass(frozen=True)
class GutenbergPublicationAdapter:
    work: dict

    def mapping(self) -> SourceMapping:
        mapping = map_public_domain_source(self.work)
        if mapping is None or mapping.provider != "project-gutenberg":
            raise ValueError("work has no Project Gutenberg source mapping")
        return mapping

    def publication(self) -> DawnPublication:
        mapping = self.mapping()
        work_id = str(self.work.get("workId") or "").strip()
        title = str(self.work.get("title") or "").strip()
        if not work_id or not title:
            raise ValueError("canonical work requires workId and title")
        authors = tuple(str(v).strip() for v in (self.work.get("authors") or []) if str(v).strip())
        languages = tuple(str(v).strip() for v in (self.work.get("languages") or []) if str(v).strip())
        reading_href = f"dawn://publication/{work_id}/source"
        return DawnPublication(
            identifier=work_id,
            title=title,
            authors=authors,
            languages=languages,
            reading_order=(PublicationLink(href=reading_href, type="text/plain", title=title, language=languages[0] if languages else None),),
            resources=(),
            toc=(),
            source={
                "provider": mapping.provider,
                "witnessId": mapping.witness_id,
                "sourceUrl": mapping.source_url,
                "accessMode": mapping.policy.mode.value,
                "materializationRequired": True,
            },
        )


def adapt_gutenberg_work(work: dict) -> DawnPublication:
    return GutenbergPublicationAdapter(work).publication()
