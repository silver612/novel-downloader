from bs4 import BeautifulSoup
import os
import requests

class Novel:
    def __init__(self, title, last_chap, details):
        self.title = title
        self.last_chapter = last_chap
        self.details = details

def get_page_content(current_page_link):
    current_page = BeautifulSoup(requests.get(current_page_link).text, 'lxml')
    novel_group = []

    novels = current_page.find_all("div",{"class":"col-12 col-md-6 badge-pos-1"})
    for novel in novels:
        novel_details = novel.find("div", {"class":"item-summary"})
        novel_title = novel_details.find("div",{"class":"post-title font-title"}).find("h3", {"class":"h5"}).text.strip()
        novel_last_chapter = novel_details.find("div",{"class":"list-chapter"}).find("span", {"class":"chapter font-meta"}).text.strip()
        novel_details_link = novel_details.find("h3", {"class":"h5"}).a["href"]
        novel_group.append(Novel(novel_title, novel_last_chapter, novel_details_link))
    
    next_page_link = current_page.find("div", {"class":"nav-previous float-left"})
    if next_page_link:
        return next_page_link.a["href"], novel_group
    else:
        return None, novel_group

def get_chapter_names(details_link):
    chapter_names = []
    details_page = BeautifulSoup(requests.get(details_link).text, 'lxml')
    chapter = 1
    chapter_link = details_link + "chapter-1/"
    chapter_page = BeautifulSoup(requests.get(chapter_link).text, 'lxml')
    while chapter_page != details_page :
        chapter_title = chapter_page.find("div", {"class":"c-breadcrumb"})
        if chapter_title != None:
            chapter_title = chapter_title.find("li", {"class":"active"}).text.strip()
        else:
            break
        chapter_names.append("Chapter " + str(chapter) + ": " + chapter_title)
        chapter = chapter + 1
        chapter_link = details_link + "/chapter-" + str(chapter) + "/"
        chapter_page = BeautifulSoup(requests.get(chapter_link).text, 'lxml')
    return chapter_names

def download_novel(details_link, filename):
    chapter = 1
    chapter_link = details_link + "chapter-1/"
    chapter_page = BeautifulSoup(requests.get(chapter_link).text, 'lxml')
    while chapter_page.find("div", {"class":"text-left"}) :
        chapter_content = chapter_page.find("div", {"class":"text-left"}).text
        with open(f"{filename}.txt","a",encoding = "utf-8") as file:
            file.write(chapter_content)
            file.write("\n\n\n")

        chapter = chapter + 1
        chapter_link = details_link + "/chapter-" + str(chapter) + "/"
        chapter_page = BeautifulSoup(requests.get(chapter_link).text, 'lxml')


all_novels_link = "https://vipnovel.com/vipnovel/?m_orderby=alphabet"
current_page_link = all_novels_link
choice = 1
novels = []

while __name__=="__main__":
    
    if int(choice)==1 : 
        _ = os.system("cls")
        if current_page_link==None:
            print("No more novels available")
        else:
            current_page_link, novels = get_page_content(current_page_link)
            for novel in novels:
                print(f"Title : {novel.title} \nLast Chapter: {novel.last_chapter} \n")
    elif int(choice)==2 :
        print("Type exact novel title (without preceding or following spaces): ")
        title = input();

        goal = None # placeholder
        for novel in novels:
            if novel.title == title:
                goal = novel
                break
        
        if goal==None:
            print("No such novel found.")
        else:
            _ = os.system("cls")
            while True:
                print(f"Novel title: {goal.title}")
                print("Actions available:")
                print("1: Get chapter list of the novel")
                print("2: Download novel")
                print("Other: Choose some other novel or To Exit")
                print("Enter choice")
                choice1 = input()

                if int(choice1) == 1:
                    chapter_names = get_chapter_names(goal.details)
                    for chapter_name in chapter_names:
                        print(chapter_name)
                elif int(choice1) == 2:
                    print("Enter file name in which to save")
                    print("Warning: If file already present, previous contents of the file will be permanently removed")
                    name = input()
                    download_novel(goal.details, name)
                    _ = os.system("cls")
                    print("Download complete")
                else:
                    break

    else:
        _ = os.system("cls")
        break
    print("Choices available:")
    if current_page_link == None:
        print("1: No more novels available")
    else:
        print("1: Display more available novels")
    print("2: Get details of a novel from above list")
    print("Any other input: Exit program")
    print("Enter choice:")
    choice = input()
    
    
