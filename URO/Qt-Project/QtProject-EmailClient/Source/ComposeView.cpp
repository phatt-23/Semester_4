//
// Created by phatt on 4/7/25.
//

#include "../Header/Views/ComposeView.h"

#include "EmailEditor.h"


ComposeView::ComposeView(const Ref<DIContainer>& diContainer, QWidget* parent, const bool isDialog)
    : QComponent("ComposeView", parent), m_DiContainer(diContainer)
    // init children
    , m_Splitter(new QSplitter(Qt::Horizontal, this))
    , m_LeftSplit(new QComponent("LeftSplit", this))
    , m_RightSplit(new QComponent("RightSplit", this))
    , m_EmailEditor(new EmailEditor(m_DiContainer, m_LeftSplit))
    , m_AttachmentSideBar(new AttachmentSideBar(m_DiContainer, m_RightSplit))
    , m_IsDialog(isDialog)
{
    // split widgets
    m_Splitter->addWidget(m_LeftSplit);
    m_Splitter->addWidget(m_RightSplit);

    m_Splitter->setSizes({400, 200});
    m_Splitter->setStretchFactor(0, 4);
    m_Splitter->setStretchFactor(1, 3);

    // layout
    const auto layout = new QVBoxLayout(this);
    layout->addWidget(m_Splitter);

    // left split
    const auto leftSplitLayout = new QVBoxLayout(m_LeftSplit);
    leftSplitLayout->addWidget(m_EmailEditor);

    if (m_IsDialog == false)
    {
        m_OpenInNewButton = new QPushButton("Open in New", m_LeftSplit);
        const auto buttonLayout = new QHBoxLayout();
        leftSplitLayout->addLayout(buttonLayout);
        buttonLayout->addStretch();
        buttonLayout->addWidget(m_OpenInNewButton);
    }

    leftSplitLayout->setStretch(0, 4);
    leftSplitLayout->setStretch(1, 0);

    // right split
    const auto rightSplitLayout = new QVBoxLayout(m_RightSplit);
    rightSplitLayout->addWidget(m_AttachmentSideBar);

    // events
    BindEvents();
}


void ComposeView::BindEvents() 
{
    connect(m_OpenInNewButton, &QPushButton::clicked, this, &ComposeView::OpenInNewButtonClicked);

    auto const bus = m_DiContainer->GetService<EventBus>();
    bus->Subscribe<SendEmailClickedEvent>([this](SendEmailClickedEvent const& e) 
    {
        auto const attchFiles = m_AttachmentSideBar->GetAttachments(); 
        auto const& emailData = m_EmailEditor->GetDataContext();
        
        // TODO: INSERT INTO email 
        qInfo() << "Insert new email" << emailData << attchFiles;
    });
}

void ComposeView::OpenInNewButtonClicked()
{
    const auto bus = m_DiContainer->GetService<EventBus>();

    const auto dialog = new QDialog();
    dialog->setWindowTitle("Compose Email");
    dialog->resize(800, 600);

    const auto composeView = new ComposeView(m_DiContainer, this, true);

    const auto dialogLayout = new QVBoxLayout(dialog);
    dialogLayout->addWidget(composeView);

    dialog->show();
}

