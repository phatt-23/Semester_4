#include "FormInserter.h"

FormInserter::FormInserter(Ref<DbContext> const& dbContext)
    : m_DbContext(dbContext)
{

}

FormInserter::~FormInserter()
{
}


bool FormInserter::InsertEmailWithAttachments(Email const& email, QStringList attachments)
{
    QSqlQuery query(m_DbContext->GetDatabase());

    query.prepare(R"(
    INSERT INTO email()

                  )");

    return true;
}
