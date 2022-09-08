import PySimpleGUI as sg
import scrape_v1 as sv


title = ""
details_link = ""
chapters = []

novels = []
current_page_link = "https://vipnovel.com/vipnovel/?m_orderby=alphabet"
try:
    while current_page_link != None:
        current_page_link, novel_set = sv.get_page_content(current_page_link)
        for n in novel_set:
            novels.append(n)
except Exception as e:
    print("Some error occurred: " + str(e))

list_panel = [
    [sg.Text("Available Novels")], 
    [sg.Listbox(values=[novel.title+">> "+novel.last_chapter for novel in novels], size=(30,30), enable_events=True, key="-BOOK LIST-", horizontal_scroll=True)]
]

layout = [list_panel]
window = sg.Window("Novel Downloader", layout, auto_size_buttons=True, auto_size_text=True)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    
    if event=="-BOOK LIST-":
        try:
            title = values["-BOOK LIST-"][0].split('>')[0]
            
            details_link = ""
            for novel in novels:
                if novel.title==title:
                    details_link = novel.details
                    break

            print("Clicked in book list: " + title + ":" + details_link)
            if len(details_link) == 0:
                download_panel = [
                    [sg.Text("Book not available", key = "-d1-")]
                ]
            else:
                download_panel = [
                    [sg.Text("Link to book: " + details_link, key = "-d1-")],
                    [sg.Text("Choose an action", key = "-d2-")],
                    [sg.Button("Download book", key="-DOWNLOAD-")], 
                    [sg.Button("See chapter list", key="-SEE CHAPTERS-")]
                ]
            
            layout_download = [download_panel]
            download_win = sg.Window("Book details", layout_download, auto_size_text=True, auto_size_buttons=True)
            
            while True:
                event,values = download_win.read()
                if event==sg.WIN_CLOSED:
                    break

                if event=="-SEE CHAPTERS-":

                    print("Clicked to see chapters")
                    chapters = sv.get_chapter_names(details_link)
                    
                    chapters_panel = [
                        [sg.Text("Available Chapters", key="-c1-", visible=False)], 
                        [sg.Listbox(values=chapters, size=(30, 30), horizontal_scroll=True)]
                    ]
                    layout_chapters = [chapters_panel]
                    chapters_win = sg.Window("View Chapters", layout_chapters)

                    while True:
                        event, values = chapters_win.read()
                        if event == sg.WIN_CLOSED:
                            break
                    
                    chapters_win.close()

                elif event=="-DOWNLOAD-":
                    print("CLicked to download novel")
                    location_panel = [
                        [
                            sg.Text("Select folder to store file: "),
                            sg.In(size=(25,1), enable_events=True, key="-FOLDER-"),
                            sg.FolderBrowse()
                        ],
                        [
                            sg.Text("Choose file name"),
                            sg.In(size=(25, 1), key="-FILE NAME-"),
                            sg.Button("Create File", key="-CREATE FILE-")
                        ]
                    ]

                    layout_location = [location_panel]
                    location_win = sg.Window("Choose File Location", layout_location)

                    while True:
                        event_, values_ = location_win.read()
                        if event_ == sg.WIN_CLOSED:
                            break
                
                        if event_=="-CREATE FILE-":
                            try:
                                filename = sv.os.path.join(values_["-FOLDER-"], values_["-FILE NAME-"])
                                print("Location: " + filename)
                                sv.download_novel(details_link, filename)
                                print("Download over")
                            except:
                                pass
                            break 

                    location_win.close()
      
            download_win.close()

        except Exception as e:
            print("Some error occurred: " + str(e))

window.close()