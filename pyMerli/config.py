import yaml


class FromFile:
    """
    """
    def __init__(self, file_path):
        """
        """
        self.file_path=file_path
        self.settings={}
        self.load()

    def load(self):
        """
        """
        fd=open(self.file_path, "r")
        self.settings=yaml.load(fd)
        fd.close()
        self.settings["countries"]=[Sites.site_id(c)
                                    for c in self.settings["countries"]]
        self.settings["categories"]=[Categories.category_id(c)
                                    for c in self.settings["categories"]]


class Sites:
    """
    """
    _base=[
        {
            "id": "MLM",
            "name": "Mexico",
            "aka":["mexico",]
        },
        {
            "id": "MPA",
            "name": "Panamá",
            "aka":["panamá", "panama"]

        },
        {
            "id": "MLV",
            "name": "Venezuela",
            "aka":["venezuela",]
        },
        {
            "id": "MPT",
            "name": "Portugal",
            "aka":["portugual",]


        },
        {
            "id": "MBO",
            "name": "Bolivia",
            "aka":["bolivia",]
        },
        {
            "id": "MLB",
            "name": "Brasil",
            "aka":["brasil","brazil"]

        },
        {
            "id": "MEC",
            "name": "Ecuador",
            "aka":["ecuador",]
        },
        {
            "id": "MPE",
            "name": "Perú",
            "aka":["perú","peru"]

        },
        {
            "id": "MGT",
            "name": "Guatemala",
            "aka":["guatemala",]
        },
        {
            "id": "MRD",
            "name": "Dominicana",
            "aka":["dominicana",
                   "republica dominicana",
                   "domenican republic"]
        },
        {
            "id": "MSV",
            "name": "El Salvador",
            "aka":["el salvador"],
        },
        {
            "id": "MLC",
            "name": "Chile",
            "aka":["chile",],
        },
        {
            "id": "MHN",
            "name": "Honduras",
            "aka":["honduras",],
        },
        {
            "id": "MLA",
            "name": "Argentina",
            "aka":["argentina",]
        },
        {
            "id": "MCU",
            "name": "Cuba",
            "aka":["cuba",],

        },
        {
            "id": "MPY",
            "name": "Paraguay",
            "aka":["paraguay",],
        },
        {
            "id": "MLU",
            "name": "Uruguay",
            "aka":["uruguay"],
        },
        {
            "id": "MNI",
            "name": "Nicaragua",
            "aka":["nicaragua"],

        },
        {
            "id": "MCO",
            "name": "Colombia",
            "aka":["colombia"],
        },
        {
            "id": "MCR",
            "name": "Costa Rica",
            "aka":["costa rica"],
        }
    ]

    @classmethod
    def site_id(cls, site_name):
        """
        """
        target_site=site_name.lower().strip()
        for site in cls._base:
            if target_site not in site["aka"]:continue
            return site["id"]
        raise Exception("[-] Unkown site: {}".format(site_name))

class Categories:
    """
    """
    _base=[
        {
        "number_id":"1051",
        "aka":[
            "celulares e telefones",
            "celulares y teléfonos"
        ]},
        {
        "number_id":"1648",
        "aka":[
            "computación",
            "informática"
        ]},
        {
        "number_id":"1144",
        "aka":[
            "games",
            "consolas y videojuegos"
        ]},
        {
        "number_id":"5726",
        "aka":[
            "electrodomésticos y aires ac.",
            "eletrodomésticos",
        ]},
        {
        "number_id":"1000",
        "aka":[
            "electrónica, audio y video",
            "eletrônicos, áudio e vídeo"
        ]},
        {
        "number_id":"1953",
        "aka":[
            "otras categorías",
            "mais Categorias"
        ]},
        {
        "number_id":"3281",
        "aka":[
            "filmes e seriados",
        ]},
        {
        "number_id":"1168",
        "aka":[
            "música y películas",
        ]},
        {
        "number_id":"1276",
        "aka":[
            "esportes e fitness",
            "deportes y fitness",
        ]},
        {
        "number_id":"1430",
        "aka":[
            "ropa, bolsas y calzado",
            "ropa y accesorios",
            "vestuario y calzado",
            "ropa, zapatos y accesorios",
            "calçados, roupas e bolsas",
        ]},
        {
        "number_id":"1384",
        "aka":[
            "bebés",
            "bebês",
            "bebes",
        ]},
        {
        "number_id":"1132",
        "aka": [
            "juegos y juguetes",
            "brinquedos e hobbies",
        ]},
        {
        "number_id":"12404",
        "aka": [
            "festas e lembrancinhas",
        ]},
        {
        "number_id":"1953",
        "aka": [
            "otras categorías",
            "mais categorias",
        ]}
    ]

    @classmethod
    def category_id(cls, category_name):
        """
        """
        target_category=category_name.lower().strip()
        for category in cls._base:
            if target_category not in category["aka"]:continue
            return category["number_id"]
        raise Exception("[-] Unkown category: {}".format(category_name))
