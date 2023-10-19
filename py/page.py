from setting import config as CF
import util.fileUtil as FILEUTIL
import util.dirUtil as DIRUTIL
from datetime import datetime


class pageUtil:
    def __init__(self, siteName, contentPath, mainPath):
        self.siteName = siteName
        self.content_soup = FILEUTIL.read_file(contentPath)
        self.content = self.content_soup.contents[2]

        self.mainContent_soup = FILEUTIL.read_file(mainPath)
        self.mainContent = self.mainContent_soup.contents[2]
        
        self.root_html='<!DOCTYPE html>\n'

        self.today=datetime.today()

        self.set_path()
        self.site_kind_proc()
        self.set_site()

    def set_path(self):
        self.svr_page_path = DIRUTIL.svr_page_path #D:\project_2023\html_template\page\
        self.file_dir_one = DIRUTIL.file_dir_one ##D:\project_2023\html_template

        self.real_aside_file_path = f'{self.svr_page_path}aside_menu.html'  #D:\project_2023\html_template\page\aside_menu.html
        self.real_footer_file_path = f'{self.svr_page_path}footer.html'     #D:\project_2023\html_template\page\footer.html
        self.real_sitemap_file_path = f'{self.file_dir_one}/sitemap.xml'   #D:\project_2023\html_template/sitemap.xml
        self.real_rotots_file_path = f'{self.file_dir_one}/robots.txt'     #D:\project_2023\html_template/robots.txt
        self.real_main_file_path = f'{self.file_dir_one}/index.html'         #D:\project_2023\html_template/index.html

        
        self.page_description =''
    



    def set_adsense(self, ad_client, ad_search, is_real=False):
        self.content.select_one(f'meta[name="adsense_client"]')['content']      = ad_client if is_real else '' 
        self.content.select_one(f'meta[name="adsense_search"]')['content']      = ad_search if is_real else '' 
        self.mainContent.select_one(f'meta[name="adsense_client"]')['content']  = ad_client if is_real else ''
        self.mainContent.select_one(f'meta[name="adsense_search"]')['content']  = ad_search if is_real else '' 


    def site_kind_proc(self):
        if not CF.SITE_KIND == 'BOOK':
            for i in ['isbn','pub_nm','pub_dt','author']:
                self.content.select_one(f'#{i}').extract()
    
    def set_site(self):
        self.mainContent.select_one('title').string = CF.SITE_NAME
        self.mainContent.select_one('link[rel="canonical"]')['href'] = CF.SITE_URL
        self.mainContent.select_one('meta[name="description"]')['content'] = CF.SITE_DESC
      
    def set_page_nm(self, order_key, ext):
        self.page_file_nm = f'{self.today.year}{self.today.month}{order_key}'
        self.ext = ext
        self.real_content_path = f'/page/{self.today.year}{self.today.month}/{self.page_file_nm}.{self.ext}'
        self.page_canonical = f'{CF.SITE_URL}{self.real_content_path}'

    
    def change_content(self, path, title_nm, img_url, content_list ):
        print("change_content start")
        self.page_title_nm = title_nm
        self.page_img_url = img_url
        
        self.page_content_text = " ".join(i for i in content_list)
        self.page_description = self.page_content_text[:200]
        
        self.content.select_one('meta[name="description"]')['content'] = self.page_content_text[:200]
        self.content.select_one('link[rel="canonical"]')['href'] = self.page_canonical

        self.content.select_one('title').string = title_nm
        self.content.select_one('#title_nm').string = title_nm
        self.content.select_one('img')['src'] = img_url

        for data in content_list:
            tag = self.content_soup.new_tag("p")
            tag.string = data
            self.content.select_one('#body_content').append(tag)

        FILEUTIL.save_file(path, f'{self.root_html}{self.content}')

        self.change_aside_menu()
        self.change_footer()
        self.change_sitemap()
        self.change_robots()
        self.change_main_page()
        print("change_content asid footer sitemap robots mainpage end")
    
    def set_book_info(self, isbn, pub_nm, pub_dt, author):
        self.content.select_one('#isbn').string  = isbn
        self.content.select_one('#pub_nm').string = pub_nm
        self.content.select_one('#pub_dt').string = pub_dt
        self.content.select_one('#author').string = author

    def change_main_page(self):
        print("change_main_page start : ", self.real_content_path )
        # self.mainContent = FILEUTIL.read_file(path)
        card_info = self.mainContent.select('.card_row_info')
        card_list = []

        card_info_max_len = len(card_info)
        
        card_list.append((self.page_title_nm, f'{self.today.year}.{self.today.month}.{self.today.day}', self.page_content_text, self.page_img_url, self.real_content_path ))
        for i in card_info:	
            card_list.append((i.select_one('.card-title').text,i.select_one('.text-muted').text,i.select_one('.card-text').text,i.img['src'], i.a['href']))
        
        for_cnt=0
        for i in range(0,card_info_max_len):
            list = card_list[for_cnt]
            self.mainContent.select_one(f'#index_title_{    for_cnt+1}').string = list[0]
            self.mainContent.select_one(f'#index_ymd_{      for_cnt+1}').string = list[1]
            self.mainContent.select_one(f'#index_content_{  for_cnt+1}').string = f'{str(list[2])[:100]}...'
            self.mainContent.select_one(f'#index_img_{      for_cnt+1}')['src'] = list[3]
            self.mainContent.select_one(f'#index_link_{     for_cnt+1}')['href'] = list[4]
            for_cnt+=1
        print("change_main_page end")
        FILEUTIL.save_file(self.real_main_file_path, f'{self.root_html}{self.mainContent}')

    def del_tag_id(self, tag_id):
        self.content.select_one(f'#{tag_id}').extract()

    def change_aside_menu(self):
        isSaveAside = True
        side = FILEUTIL.file_open_text(self.real_aside_file_path)
        side = side.replace('templeSiteName',self.siteName)      
        new_data = ''

        add_menu_sub = f'<li class="menu-item"><a href="{self.real_content_path}" class="menu-link"><div data-i18n="{self.page_title_nm}">{self.page_title_nm}</div></a></li>'
        if side.find(f'<div data-i18n="{self.today.year}{self.today.month}">') == -1:
            menu_item_location = side.find('<li class="menu-item open">')
            new_data += side[:menu_item_location]
            new_data += f'<li class="menu-item open"><a href="javascript:void(0)" class="menu-link menu-toggle"><i class="menu-icon tf-icons bx bx-dock-top"></i><div data-i18n="{self.today.year}{self.today.month}">{self.today.year}{self.today.month}</div></a><ul class="menu-sub">{add_menu_sub}</ul>'
            new_data += side[menu_item_location:].replace('open','')

        elif side.find(f'{self.real_content_path}') == -1:
            menu_sub_location = side.find('<ul class="menu-sub">')+len('<ul class="menu-sub">')
            new_data += side[:menu_sub_location] 
            new_data += add_menu_sub
            new_data += side[menu_sub_location:]
        else:
            isSaveAside = False


        if isSaveAside:
            FILEUTIL.save_file(self.real_aside_file_path, new_data)
    
    def init_page(self, tp_path, page_path):
        FILEUTIL.save_file(page_path, FILEUTIL.file_open_text(tp_path))

    
    def change_sitemap(self, origin=False):
        sitemap_data = FILEUTIL.file_open_text(self.real_sitemap_file_path)
        new_data =''
        new_data = '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'

        if not origin:
            if sitemap_data.find(self.real_content_path) == -1:
                first_idx = len(new_data)
                new_data += f'<url><loc>{CF.SITE_URL}{self.real_content_path}</loc><lastmod>{self.today.year}-{self.today.month}-{self.today.day}</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>'

        new_data += '</urlset>'  
        FILEUTIL.save_file(self.real_sitemap_file_path, new_data)

    def change_robots(self):
        FILEUTIL.save_file(self.real_rotots_file_path, f'User-agent: * \nDisallow: /tp \nDisallow: /py \nAllow:/ \n\nSitemap: {CF.SITE_URL}/sitemap.xml')

    def change_footer(self):
        footer_copyrigth = f'©{CF.SITE_NAME} {self.today.year} All rights reserved'

        footer_data = FILEUTIL.file_open_text(self.real_footer_file_path)
        new_data = footer_data[:footer_data.find('f_text')+len('f_text')+2]
        new_data += footer_copyrigth
        new_data += '</div></footer>'
        FILEUTIL.save_file(self.real_footer_file_path, new_data)
