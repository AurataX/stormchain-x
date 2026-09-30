from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import session
from app.core.security import require_operator
from app.schemas.briefing import BriefingInput, BriefingOutput
from app.services.briefing_context import gather
from app.services.briefing_lookup import select_sources
from app.services.vertex_briefing import generate

router = APIRouter(prefix="/api/v1/briefings", tags=["Briefings"])
Database = Annotated[AsyncSession, Depends(session)]


@router.post("", response_model=BriefingOutput, dependencies=[Depends(require_operator)])
async def briefing(payload: BriefingInput, request: Request, db: Database):
    plan, sources = await gather(db, payload)
    sources = await select_sources(request.app.state.settings, payload.question, sources)
    draft = await generate(request.app.state.settings, payload.question, sources)
    return BriefingOutput(
        answer=draft.answer,
        citation_ids=draft.citation_ids,
        sources={key: sources[key] for key in draft.citation_ids},
        plan_id=payload.plan_id,
        plan_version=plan.version,
        model=request.app.state.settings.vertex_model,
    )
