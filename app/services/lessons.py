from app.models.lessons_reports import LessonReport

class LessonReportService:
    def __init__(self, repository):
        self.repository = repository

    async def get_lesson_reports_by_student_id(self, student_id):
        return await self.repository.get_lesson_reports_by_student_id(student_id)

    async def create_report(self, report_data):
        return await self.repository.create_report(report_data)

    async def get_report_by_id(self, report_id): 
        return await self.repository.get_report_by_id(report_id)

    async def update_report(self, report_id, report_data): 
        return await self.repository.update_report(report_id, report_data)