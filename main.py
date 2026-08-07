import flet as ft
import os

def main(page: ft.Page):
    page.title, page.theme_mode, page.bgcolor = "Pence Manga", ft.ThemeMode.DARK, "#121212"
    page.window_width, page.window_height, page.window_resizable, page.padding = 390, 844, False, 0
    
    base_dir = os.path.dirname(__file__)

    # Наша база данных (Каталог + Локальные картинки страниц)
    manga_list = [
        {
            "id": "blade", "title": "Клинок", "genres": "Фэнтези", "rating": "4.8", 
            "cover": os.path.join(base_dir, "blade.jpg"), 
            "desc": "Эпоха Тайсё. Тандзиро Камадо отправляется в опасный путь, чтобы вернуть сестре человеческий облик!",
            "chapters": ["Глава 1: Жестокость", "Глава 2: Незнакомец"],
            # Читалка будет брать страницы из твоей папки manga_pages!
            "pages": [os.path.join(base_dir, "manga_pages", "page1.jpg"), os.path.join(base_dir, "manga_pages", "page2.jpg"), os.path.join(base_dir, "manga_pages", "page3.jpg")]
        },
        {
            "id": "titans", "title": "Титаны", "genres": "Ужасы", "rating": "4.9", 
            "cover": os.path.join(base_dir, "titans.jpg"), 
            "desc": "Человечество ведет кошмарную борьбу за выживание против гигантских гуманоидов — Титанов.",
            "chapters": ["Глава 1: К тебе, спустя две тысячи лет", "Глава 2: Тот день"],
            "pages": [os.path.join(base_dir, "manga_pages", "page1.jpg"), os.path.join(base_dir, "manga_pages", "page2.jpg"), os.path.join(base_dir, "manga_pages", "page3.jpg")]
        },
        {
            "id": "onepunch", "title": "Ванпанчмен", "genres": "Комедия", "rating": "4.7", 
            "cover": os.path.join(base_dir, "onepunch.jpg"), 
            "desc": "История о Сайтаме, который обрел силу побеждать абсолютно любого врага с одного удара!",
            "chapters": ["Глава 1: Один удар", "Глава 2: Тренировки"],
            "pages": [os.path.join(base_dir, "manga_pages", "page1.jpg"), os.path.join(base_dir, "manga_pages", "page2.jpg"), os.path.join(base_dir, "manga_pages", "page3.jpg")]
        }
    ]
    
    page.data = {"manga": None, "idx": 0}

    # Элементы читалки
    ch_title = ft.Text(size=16, color="white", weight=ft.FontWeight.BOLD)
    p_count = ft.Text("1 / 1", size=16, color="white")
    img = ft.Image(src="", width=390, height=560, fit="contain")
    
    def refresh_page():
        if os.path.exists(page.data["manga"]["pages"][page.data["idx"]]):
            img.src = page.data["manga"]["pages"][page.data["idx"]]
        else:
            # Если страниц в папке нет, покажем обложку как заглушку, чтобы не было серого экрана
            img.src = page.data["manga"]["cover"]
        p_count.value = f"{page.data['idx'] + 1} / {len(page.data['manga']['pages'])}"
        page.update()

    def next_page(e):
        if page.data["manga"] and page.data["idx"] < len(page.data["manga"]["pages"]) - 1:
            page.data["idx"] += 1
            refresh_page()

    def prev_page(e):
        if page.data["manga"] and page.data["idx"] > 0:
            page.data["idx"] -= 1
            refresh_page()

    def toggle(to_catalog):
        details_container.visible = not to_catalog
        catalog.visible = to_catalog
        if to_catalog: reader.visible = False
        page.update()

    # Экран самого плеера страниц
    reader = ft.Column([
        ft.Container(ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda e: toggle(True)), ch_title]), bgcolor="#1A1A1A", padding=4),
        ft.Container(img, alignment="center", height=560),
        ft.Container(ft.Row([
            ft.IconButton(ft.Icons.ARROW_LEFT, icon_color="white", icon_size=36, on_click=prev_page), 
            p_count, 
            ft.IconButton(ft.Icons.ARROW_RIGHT, icon_color="white", icon_size=36, on_click=next_page)
        ], alignment=ft.MainAxisAlignment.SPACE_AROUND), bgcolor="#1A1A1A", padding=10)
    ], visible=False)

    # Экран списка глав
    det_title = ft.Text(size=22, weight=ft.FontWeight.BOLD, color="white")
    det_chapters = ft.Column(spacing=10)
    
    def start_read(title, manga):
        page.data["manga"] = manga
        page.data["idx"] = 0
        ch_title.value = title
        details_container.visible = False
        reader.visible = True
        refresh_page()

    def open_manga(manga):
        det_title.value = manga["title"]
        det_chapters.controls = [
            ft.Container(
                content=ft.Row([ft.Icon(ft.Icons.MENU_BOOK, color="white"), ft.Text(f"Глава {i+1}", size=14, color="white")]),
                bgcolor="#1E1E1E", padding=12, border_radius=10, 
                on_click=lambda e, t=f"Глава {i+1}": start_read(t, manga)
            ) for i in range(2)
        ]
        toggle(False)

    details_content = ft.Column([
        ft.IconButton(ft.Icons.ARROW_BACK_IOS, icon_color="white", on_click=lambda e: toggle(True)),
        det_title, 
        ft.Container(ft.Text("Список глав:", size=16, color="#FF7A00"), padding=10), 
        det_chapters
    ])
    
    details_container = ft.Container(content=details_content, padding=16, visible=False)

    # Главный каталог манги
    cards = ft.Column([
        ft.Container(
            content=ft.Row([
                ft.Container(ft.Image(m["cover"], width=100, height=140, fit="contain"), border_radius=12), 
                ft.Column([ft.Text(m["title"], size=16, weight=ft.FontWeight.BOLD, color="white"), ft.Text(m["genres"], size=12, color="grey"), ft.Text(f"⭐ {m['rating']}", size=14, color="white")], spacing=6)
            ], spacing=14), 
            bgcolor="#1E1E1E", padding=12, border_radius=18, 
            on_click=lambda e, m=m: open_manga(m)
        ) for m in manga_list
    ], spacing=14)
    
    catalog = ft.Column([
        ft.Container(ft.Text("Pence Manga", size=26, weight=ft.FontWeight.BOLD, color="#FF7A00"), bgcolor="#1A1A1A", padding=16), 
        ft.Container(cards, padding=16)
    ])
    
    page.add(ft.ListView([catalog, details_container, reader], expand=True))

# ИСПРАВЛЕНО: добавили жесткую привязку ресурсов для мобильного компилятора!
ft.app(target=main, assets_dir=".")
