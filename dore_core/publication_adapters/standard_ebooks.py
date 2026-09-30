"""Standard Ebooks -> DawnPublication adapter.

Standard Ebooks is the first provider allowed to continue through Doré's
remote materialization route. The Reader still receives only DawnPublication;
provider details stay behind this adapter and WitnessAccessPolicy.
"""
from __future__ import annotations

from dataclasses import dataclass

from dore_core.language.source_mapping import SourceMapping, map_public_domain_source
from dore_core.publication import DawnPublication, PublicationLink


@dataclass(frozen=True)
class StandardEbooksPublicationAdapter:
    work: dict

    def mapping(self) -> SourceMapping:
        mapping = map_public_domain_source(self.work)
        if mapping is None or mapping.provider != "standard-ebooks":
            raise ValueError("work has no Standard Ebooks source mapping")
        if not mapping.policy.may_retrieve_automatically():
            raise ValueError("Standard Ebooks source is not authorized for remote materialization")
        return mapping

    def publication(self) -> DawnPublication:
        mapping = self.mapping()
        work_id = str(self.work.get("workId") or "").strip()
        title = str(self.work.get("title") or "").strip()
        if not work_id or not title:
            raise ValueError("canonical work requires workId and title")
        authors = tuple(str(v).strip() for v in (self.work.get("authors") or []) if str(v).strip())
        languages = tuple(str(v).strip() for v in (self.work.get("languages") or []) if str(v).strip())
        href = f"dawn://publication/{work_id}/source"
        return DawnPublication(
            identifier=work_id,
            title=title,
            authors=authors,
            languages=languages,
            reading_order=(PublicationLink(href=href, type="application/epub+zip", title=title, language=languages[0] if languages else None),),
            source={
                "provider": mapping.provider,
                "witnessId": mapping.witness_id,
                "sourceUrl": mapping.source_url,
                "accessMode": mapping.policy.mode.value,
                "automatedAccess": True,
                "persistentCache": mapping.policy.may_persist_retrieved_text(),
                "materializationRequired": True,
            },
        )


def adapt_standard_ebooks_work(work: dict) -> DawnPublication:
    return StandardEbooksPublicationAdapter(work).publication()
