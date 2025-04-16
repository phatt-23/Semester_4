#ifndef INCLUDE_DATABASE_FORMINSERTER_H_
#define INCLUDE_DATABASE_FORMINSERTER_H_




#include "DataModels.h"
#include "DbContext.h"
#include "IService.h"
#include "StdLib.h"




/// handles non-trivial insertion to the database
class FormInserter : public IService
{
public:
    FormInserter(Ref<DbContext> const& dbContext);
    ~FormInserter() override;

    /// should be async
    bool InsertEmailWithAttachments(Email const& email, QStringList attachments); 

private:
    Ref<DbContext> m_DbContext;
};



#endif  // INCLUDE_DATABASE_FORMINSERTER_H_



