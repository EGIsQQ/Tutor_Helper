from app.models.lessons_reports import LessonReport
from sqlalchemy import select
from sqlalchemy.orm import joinedload

class LessonReportRepository:
    def __init__(self, session):
        self.session = session

    async def get_lesson_reports_by_student_id(self, student_id):
        result = await self.session.execute(
            select(LessonReport)
            .where(LessonReport.student_id == student_id)
            .order_by(LessonReport.lesson_date.desc())
        )
        return result.scalars().all()

    async def create_report(self, report_data): 
        self.session.add(report_data)
        await self.session.commit()

    async def get_report_by_id(self, report_id): 
        result = await self.session.execute(
        select(LessonReport)
        .options(joinedload(LessonReport.student))
        .where(LessonReport.id == report_id))

        return result.scalars().first()

    async def update_report(self, report_id, report_data): 
        report = await self.get_report_by_id(report_id)
                
        update_data = report_data.model_dump(
        exclude_unset=True)

        for field, value in update_data.items():
            if field == "lesson_date" and value is not None:
                value = value.replace(tzinfo=None)
                
            setattr(report, field, value)

        await self.session.commit()
        await self.session.refresh(report)

        return report