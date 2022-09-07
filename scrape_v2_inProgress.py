import PySimpleGUI as sg
import scrape_v1 as sv


novels = []
current_page_link = "https://vipnovel.com/vipnovel/?m_orderby=alphabet"
try:
    while current_page_link != None:
        current_page_link, novel_set = sv.get_page_content(current_page_link)
        for n in novel_set:
            novels.append(n)
except:
    pass

list_panel = [
    [sg.Text("Available Novels")], 
    [sg.Listbox(values=[novel.title+" >> "+novel.last_chapter for novel in novels], size=(30,30), enable_events=True, key="-BOOK LIST-", horizontal_scroll=True)]
]

download_panel = [
    sg.Column([[sg.Text("Link to book: ", key = "-d1-", size=(25,2), visible=False)],
    [sg.Text("Choose an action", key = "-d2-", size=(15,2), visible=False)],
    [sg.Button("Download book", key="-DOWNLOAD-", visible=False)], 
    [sg.Button("See chapter list", key="-SEE CHAPTERS-", visible=False)],
    [sg.Button("Close this panel", key="-RECHOOSE-", visible=False)]], size=(30, 30))
]

chapters_panel = [
    [sg.Text("Available Chapters", key="-c1-", visible=False)], 
    [sg.Listbox(values=[], size=(30, 30), enable_events=True, key="-CHAPTERS-", horizontal_scroll=True)],
    [sg.Button("Back", key="-BACK-", visible=False)]
]

location_panel = [
    [
        sg.Text("Select folder to store file: "),
        sg.In(size=(25,1), enable_events=True, key="-FOLDER-", default_text="C:\\Program Files\\Novel Downloader"),
        sg.FolderBrowse()
    ],
    [
        sg.Text("Choose file name"),
        sg.In(size=(25, 1), key="-FILE NAME-"),
        sg.Button("Create File", key="-CREATE FILE-")
    ]
]

layout = [
    [list_panel,
    sg.VSeparator(),
    download_panel,
    chapters_panel]
]

layout_popup = [location_panel]


window = sg.Window("Novel Downloader", layout, size=(1000,500), location=(0,0))

title = ""
details_link = ""
chapters = []

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    
    if event=="-BOOK LIST-" or event=="-BACK-":
        try:
            if event=="-BOOK LIST-":
                title = values["-BOOK LIST-"][0].split('>')[0]
                
                details_link = ""
                for novel in novels:
                    if novel.title==title:
                        details_link = novel.details
                        break

            window["-c1-"].Update(visible=False)
            window["-CHAPTERS-"].Update(visible=False)
            window["-BACK-"].Update(visible=False)
            
            print("Clicked in book list: " + details_link)
            print(window["-d1-"].get_size())
            if details_link=="":
                window["-d1-"].Update(text="Book not available")
                window["-d1-"].Update(visible=True)
            else:
                window["-d1-"].Update(text="Link to book: " + details_link)
                window["-d1-"].Update(visible=True)
                window["-d2-"].Update(visible=True)
                window["-DOWNLOAD-"].Update(visible=True)
                window["-SEE CHAPTERS-"].Update(visible=True)
                window["-RECHOOSE-"].Update(visible=True)
        except:
            pass

    elif event=="-RECHOOSE-":
        title = ""
        window["-d1-"].Update(visible=False)
        window["-d2-"].Update(visible=False)
        window["-DOWNLOAD-"].Update(visible=False)
        window["-SEE CHAPTERS-"].Update(visible=False)
        window["-RECHOOSE-"].Update(visible=False)

    elif event=="-SEE CHAPTERS-":
        window["-d1-"].Update(visible=False)
        window["-d2-"].Update(visible=False)
        window["-DOWNLOAD-"].Update(visible=False)
        window["-SEE CHAPTERS-"].Update(visible=False)
        window["-RECHOOSE-"].Update(visible=False)

        try:
            chapters = sv.print_chapter_names(details_link)
            window["-c1-"].Update(visible=True)
            window["-CHAPTERS-"].Update(values=chapters)
            window["-CHAPTERS-"].Update(visible=True)
            window["-BACK-"].Update(visible=True)
        except:
            pass

    elif event=="-DOWNLOAD-":
        window["-d1-"].Update(visible=False)
        window["-d2-"].Update(visible=False)
        window["-DOWNLOAD-"].Update(visible=False)
        window["-SEE CHAPTERS-"].Update(visible=False)
        window["-RECHOOSE-"].Update(visible=False)

        location = sg.Window("Choose File Location", layout_popup)

        while True:
            event_, values_ = location.read()
            if event_ == sg.WIN_CLOSED:
                break
    
            if event_=="-CREATE FILE-":
                try:
                    filename = sv.os.path.join(values_["-FOLDER-"], values_["-FILE NAME-"])
                    sv.download_novel(details_link, filename)
                except:
                    pass
                break 

        location.close()
       

window.close()