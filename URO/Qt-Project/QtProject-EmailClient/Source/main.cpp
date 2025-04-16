
#include "DIContainer.h"
#include "Event/EventBus.h"
#include "MainWindow.h"
#include "StdLib.h"
#include "Database/DbContext.h"
#include "Database/EmailRepo.h"
#include <QApplication>

#include "Database/AttachmentRepo.h"
#include "Database/UserRepo.h"


int main(int argc, char** argv)
{
    QApplication app(argc, argv);


    // Event bus service.
    const auto eventBusService = CreateRef<EventBus>();


    // Database context.
    const auto dbService = CreateRef<DbContext>();
    if (!dbService->Connect("Assets/Sql/emails.db")) {
        qFatal("Failed to connect to DB.");
    }


    // Database repos.
    const auto emailRepo = CreateRef<EmailRepo>(dbService);
    const auto userRepo = CreateRef<UserRepo>(dbService);
    const auto attachmentRepo = CreateRef<AttachmentRepo>(dbService);


    // Set up DI Container and add services.
    const auto diContainer = CreateRef<DIContainer>();
    diContainer->AddSingleton<Ref<EventBus>>(eventBusService);
    diContainer->AddSingleton<Ref<DbContext>>(dbService);
    diContainer->AddSingleton<Ref<EmailRepo>>(emailRepo);
    diContainer->AddSingleton<Ref<UserRepo>>(userRepo);
    diContainer->AddSingleton<Ref<AttachmentRepo>>(attachmentRepo);


    // Inject DI container.
    MainWindow window(diContainer);
    window.setWindowTitle("Qt Email Client");
    window.resize(1200, 800);
    window.show();


    // Run.
    return QApplication::exec();
}

