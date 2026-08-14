from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import re

from bs4 import BeautifulSoup

URL = "http://normas.receita.fazenda.gov.br/sijut2consulta/consulta.action"

def fetch_html() -> bytes:
    request = Request(
        URL,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/58.0.3029.110"
        })

    try:
        with urlopen(request, timeout=30) as response:
             return response.read()
        
    except HTTPError as error:
        raise FederalRevenueUnavailableError(
            f"Receita Federal respondeu com status {error.code}"
        ) from error

    except URLError as error:
        raise FederalRevenueUnavailableError(
            "Não foi possível conectar ao site da Receita Federal"
        ) from error

    except TimeoutError as error:
        raise FederalRevenueUnavailableError(
            "Tempo limite excedido ao acessar a Receita Federal"
        ) from error

def parse_norms(html: bytes) -> list[dict]:
    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    table = soup.find(
        "table",
        id="tabelaAtos"
    )

    if table is None:
        raise FederalRevenueInvalidResponseError(
            "A estrutura da página foi alterada"
        )

    rows = table.find_all(
        "tr",
        class_="linhaResultados"
    )

    norms = []

    for row in rows:
        columns = row.find_all("td")

        if len(columns) < 5:
            continue

        source_id = extract_source_id(row)

        norm = {
            "source_id": source_id,
            "act_type": columns[0].get_text(" ", strip=True),
            "act_number": int(columns[1].get_text(strip=True)),
            "agency_unit": columns[2].get_text(" ", strip=True),
            "publication": columns[3].get_text(strip=True),
            "summary": columns[4].get_text(" ", strip=True),
        }

        norms.append(norm)

    return norms

def scrape_norms() -> list[dict]:
    html = fetch_html()

    return parse_norms(html)

def extract_source_id(row) -> int | None:
    link = row.find("a", href=True)

    if link is None:
        return None

    href = link["href"]

    match = re.search(
         r"/consulta/externa/(\d+)",
         href
    )

    if match is None:
        return None

    return int(match.group(1))

class FederalRevenueUnavailableError(Exception):
    pass


class FederalRevenueInvalidResponseError(Exception):
    pass