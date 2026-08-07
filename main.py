import flet as ft
import os

def main(page: ft.Page):
    page.title, page.theme_mode, page.bgcolor = "Pence Manga", ft.ThemeMode.DARK, "#0B0C10"
    page.window_width, page.window_height, page.window_resizable, page.padding = 390, 844, False, 0
    
    base_dir = os.path.dirname(__file__)

    # НАШ ТРЕНДОВЫЙ ФИОЛЕТОВЫЙ ЦВЕТ (Вместо оранжевого)
    PURPLE = "#9D4EDD"

    manga_list = [
        {
            "id": "blade", "title": "Клинок", "genres": "Экшен, Фэнтези", "rating": "4.8", 
            "cover": os.path.join(base_dir, "blade.jpg"), 
            "desc": "Эпоха Тайсё. Тандзиро Камадо отправляется в опасный путь, чтобы вернуть сестре человеческий облик!",
            "chapters": ["Глава 1: Жестокость", "Глава 2: Незнакомец"],
            "pages": [os.path.join(base_dir, "manga_pages", "page1.jpg"), os.path.join(base_dir, "manga_pages", "page2.jpg"), os.path.join(base_dir, "manga_pages", "page3.jpg")]
        },
        {
            "id": "titans", "title": "Титаны", "genres": "Экшен, Ужасы", "rating": "4.9", 
            "cover": os.path.join(base_dir, "titans.jpg"), 
            "desc": "Человечество ведет кошмарную борьбу за выживание против гигантских гуманоидов — Титанов.",
            "chapters": ["Глава 1: К тебе, спустя две тысячи лет", "Глава 2: Тот день"],
            "pages": [os.path.join(base_dir, "manga_pages", "page1.jpg"), os.path.join(base_dir, "manga_pages", "page2.jpg"), os.path.join(base_dir, "manga_pages", "page3.jpg")]
        },
        {
            "id": "onepunch", "title": "Ванпанчмен", "genres": "Экшен, Комедия", "rating": "4.7", 
            "cover": os.path.join(base_dir, "onepunch.jpg"), 
            "desc": "История о Сайтаме, который обрел силу побеждать абсолютно любого врага с одного удара!",
            "chapters": ["Глава 1: Один удар", "Глава 2: Тренировки"],
            "pages": [os.path.join(base_dir, "manga_pages", "page1.jpg"), os.path.join(base_dir, "manga_pages", "page2.jpg"), os.path.join(base_dir, "manga_pages", "page3.jpg")]
        }
    ]
    
    page.data = {"manga": None, "idx": 0}

    # ---------- ЭКРАН ЧТЕНИЯ (ПОСТРАНИЧНЫЙ ПЛЕЕР) ----------
    reader_title = ft.Text(size=16, color="white", weight=ft.FontWeight.BOLD)
    p_count = ft.Text("1 / 1", size=16, color="white", weight=ft.FontWeight.BOLD)
    img = ft.Image(src="", width=390, height=500, fit="contain")
    
    def refresh_page():
        if os.path.exists(page.data["manga"]["pages"][page.data["idx"]]):
            img.src = page.data["manga"]["pages"][page.data["idx"]]
        else:
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

    reader = ft.Column([
        ft.Container(ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda e: toggle(False)), reader_title]), bgcolor="#1F2128", padding=4),
        ft.Container(img, alignment="center", height=500),
        ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.IconButton(ft.Icons.ARROW_LEFT_ROUNDED, icon_color="white", icon_size=36, on_click=prev_page), 
                    p_count, 
                    ft.IconButton(ft.Icons.ARROW_RIGHT_ROUNDED, icon_color="white", icon_size=36, on_click=next_page)
                ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                ft.Row([
                    ft.TextButton(content=ft.Text("Предыдущая", color="grey", size=14), on_click=prev_page),
                    ft.TextButton(content=ft.Text("Следующая", color=PURPLE, size=14, weight="bold"), on_click=next_page),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ]), bgcolor="#1F2128", padding=12
        )
    ], visible=False)

    # ---------- ЭКРАН ДЕТАЛЬНОГО ОПИСАНИЯ АНИМЕ ----------
    det_cover = ft.Image(src="", width=100, height=140, fit="contain", border_radius=12)
    det_title = ft.Text(size=20, weight=ft.FontWeight.BOLD, color="white", max_lines=2)
    det_genres = ft.Text(size=14, color="grey")
    det_rating = ft.Text(size=16, weight=ft.FontWeight.W_600, color="white")
    det_desc = ft.Text(size=14, color="white")
    det_chapters = ft.Column(spacing=10)

    def start_read(title, manga):
        page.data["manga"] = manga
        page.data["idx"] = 0
        reader_title.value = title
        details_container.visible = False
        reader.visible = True
        refresh_page()

    def open_manga(manga):
        det_cover.src = manga["cover"]
        det_title.value = manga["title"]
        det_genres.value = manga["genres"]
        det_rating.value = manga["rating"]
        det_desc.value = manga["desc"]

        det_chapters.controls = [
            ft.Container(
                content=ft.Row([ft.Icon(ft.Icons.MENU_BOOK, color="white", size=18), ft.Text(f"Глава {i+1}", size=14, color="white")], spacing=10),
                bgcolor="#1F2128", padding=12, border_radius=10, 
                on_click=lambda e, t=f"Глава {i+1}": start_read(t, manga)
            ) for i in range(len(manga["chapters"]))
        ]
        toggle(False)

    details_content = ft.Column([
        ft.IconButton(ft.Icons.ARROW_BACK_IOS, icon_color="white", on_click=lambda e: toggle(True)),
        ft.Row([
            det_cover,
            ft.Column([
                det_title,
                det_genres,
                ft.Row([ft.Icon(ft.Icons.STAR_ROUNDED, color="#FFC107", size=20), det_rating], spacing=4)
            ], expand=True, spacing=6)
        ], spacing=14, vertical_alignment=ft.CrossAxisAlignment.START),
        ft.Container(ft.Text("Сюжет", size=18, weight=ft.FontWeight.BOLD, color=PURPLE), padding=ft.Padding(0, 10, 0, 0)),
        det_desc,
        ft.Container(ft.Text("Список глав:", size=18, weight=ft.FontWeight.BOLD, color=PURPLE), padding=ft.Padding(0, 10, 0, 5)),
        det_chapters
    ])
    
    details_container = ft.Container(content=details_content, padding=16, visible=False)

    # ---------- ГЛАВНЫЙ КАТАЛОГ МАНГИ ----------
    cards = ft.Column([
        ft.Container(
            content=ft.Row([
                ft.Container(ft.Image(m["cover"], width=100, height=140, fit="contain"), border_radius=12), 
                ft.Column([ft.Text(m["title"], size=16, weight=ft.FontWeight.BOLD, color="white"), ft.Text(m["genres"], size=12, color="grey"), ft.Text(f"⭐ {m['rating']}", size=14, color="white")], spacing=6)
            ], spacing=14), 
            bgcolor="#1F2128", padding=12, border_radius=18, 
            on_click=lambda e, m=m: open_manga(m)
        ) for m in manga_list
    ], spacing=14)
    
    catalog = ft.Column([
        ft.Container(ft.Text("Pence Manga", size=26, weight=ft.FontWeight.BOLD, color=PURPLE), bgcolor="#1F2128", padding=16), 
        ft.Container(cards, padding=16)
    ])
    
    page.add(ft.ListView([catalog, details_container, reader], expand=True))

ft.app(target=main, assets_dir=".")
