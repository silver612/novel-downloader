import os
import requests
import re
from bs4 import BeautifulSoup

class Novel:
    def __init__(self, title, chapter_count, status, details):
        self.title = title
        self.chapter_count = chapter_count
        self.status = status
        self.details = details

class Chapter:
    def __init__(self, title, link):
        self.title = title
        self.link = link

def get_list_all(Novels):
    all_link = "https://www.lightnovelpub.com/browse"
    current_page_link = all_link
    while current_page_link:
        Novel_cluster = []
        current_page = BeautifulSoup(requests.get(current_page_link, headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}).text, "lxml")
        next_page_link = current_page.find("div",{"class":"pagination-container"}).find("li",{"class":"PagedList-skipToNext"})
        if next_page_link:
            next_page_link = "https://www.lightnovelpub.com" + next_page_link.a["href"]
        else:
            break
        novels = current_page.find_all("li",{"class":"novel-item"})
        #print(len(novels))
        for novel in novels:
            novel_title = novel.find("h4")
            if novel_title:
                novel_title = novel_title.text.strip()
                novel_chapter_count = novel.find_all("div",{"class":"novel-stats"})[1].find_all("span")[1].text.strip()
                novel_status = novel.find_all("div",{"class":"novel-stats"})[3].find("span").text.strip()
                novel_details_link = "https://www.lightnovelpub.com" + novel.find("h4").a["href"]
                Novel_cluster.append(Novel(novel_title,novel_chapter_count,novel_status,novel_details_link))
        current_page_link = next_page_link
        Novels.append(Novel_cluster) 
    return Novels

def get_chapter_list(details_link):
    contents_list = []
    #details_link = "https://www.lightnovelpub.com/novel/trash-count-wn-17031322"
    while details_link:
        details_html = requests.get(details_link, headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"})
        details_html = details_html.text
        details_soup = BeautifulSoup(details_html, "lxml")
        chapter_cluster = []
        for chapter_list in details_soup.find("ul",{"class":"chapter-list"}).find_all("li"):
            chapter = Chapter(chapter_list.a["title"], "https://www.lightnovelpub.com"+ chapter_list.a["href"])
            chapter_cluster.append(chapter)
        contents_list.append(chapter_cluster)
        details_link =  details_soup.find("li",{"class":"PagedList-skipToNext"})
        if details_link:
            details_link = "https://www.lightnovelpub.com" + details_link.a["href"]
        if not(details_link):
            break
    return contents_list

def get_chapter(chapter, filename):
    #chapter_link = "https://www.lightnovelpub.com/novel/trash-count-wn-17031322/chapter-1"
    chapter_link = chapter.link
    chapter_html = requests.get(chapter_link, headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"})
    chapter_html = chapter_html.text
    chapter_soup = BeautifulSoup(chapter_html, "lxml")
    page_contents = chapter_soup.find("div", {"id":"chapter-container"}).find_all("p",{"class":""})
    with open(f"{filename}.txt","a",encoding = "utf-8") as slot:
        slot.write(chapter.title)
        slot.write("\n\n")
        for paragraph in page_contents:
            line = paragraph.text
            slot.write(line)
            slot.write("\n")
        slot.write("\n\n")

def get_chapters(filename, chapters, begin_at, end_at):
    open(f"{filename}.txt","w").close()
    for index in range(begin_at, end_at+1):
        get_chapter(chapters[index-1],filename)


available_list = []
available_list = get_list_all(available_list)
while __name__ == "__main__":
    print("Choices available:")
    print("1: Display all available novels")
    print("2: Get details of a novel")
    print("3: Exit program")
    print("Enter choice:")
    choice = int(input())
    _ = os.system("cls")

    if choice == 1:
        for cluster in available_list:
            for cell in cluster:
                print(f"Title : {cell.title} \nChapter count: {cell.chapter_count} Novel status: {cell.status}")
            
            print()
            print("To see the next group of novels, print Y or y. All other values will cause an exit from the list")
            choice1 = input()
            _ = os.system("cls")

            if choice1 == 'Y' or choice1 == 'y':
                continue
            else:
                break
    
    elif choice == 2:
        print("Enter the exact title of the novel you wish to download")
        novel = []
        novel_title = input()
        _ = os.system("cls")
        for cluster in available_list:
            for cell in cluster:
                if cell.title == novel_title:
                    novel = cell
                    break
        if novel == 0:
            print("Novel not found. Please re-check the title is exactly the same as that in the novel list shown.")
            break
        
        chapter_list = get_chapter_list(novel.details)
        chapters = []
        for chapter_cluster in chapter_list:
            for chapter in chapter_cluster:
                chapters.append(chapter)
    
        while __name__ == "__main__":
            
            print("Actions available:")
            print("1: Get chapter list of the novel")
            print("2: Download some sections of the novel")
            print("3: Choose some other novel")
            print("Enter choice")
            choice1 = int(input())
            _ = os.system("cls")

            if choice1 == 1 :
                print("Chapter list of the novel requested:")
                index = 1
                for chapter_cluster in chapter_list:
                    for chapter in chapter_cluster:
                        print("index:", index, chapter.title)
                        index = index + 1
                    print()
                    print("To see the next group of chapters, print Y or y. All other values will cause an exit from the list")
                    choice2 = input()
                    _ = os.system("cls")

                    if choice2 == 'Y' or choice2 == 'y':
                        continue
                    else:
                        break

            elif choice1 == 2:
                print("Enter chapter number at beginning of section you wish to download:")
                begin = int(input())
                while begin not in range(1,len(chapters)+1):
                    print("Invalid value. Please select correctly")
                    begin = int(input())
                print("Enter chapter number of ending of section you wish to download:")
                end = int(input())
                while end not in range(1,len(chapters)+1):
                    print("Inalid value. Please select correctly")
                    end = int(input())
                print("Enter exact filename where you wish to see your downloaded content:")
                print("(Warning: Previous contents of the file will be permanently removed)")
                filename = input()
                get_chapters(filename, chapters, begin, end)
                _ = os.system("cls")
                print("Download complete")

            elif choice1 == 3:
                print("Novel unselected")
                break

            else:
                print("Action not available. Please re-choose correctly.")
    
    elif choice == 3:
        print("Exited from program.")
        break

    else:
        print("Choice not available. Please re-choose correctly.")