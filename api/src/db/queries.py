"""
Low-level Neo4j query functions.

Every function accepts a ``Session`` and returns plain Python dicts / lists.
No business logic lives here — only Cypher.
"""

from neo4j import Session
from typing import Optional

def fetch_all_graphs(session: Session) -> list[dict]:
    """
    Return summary information for every ExpertiseMap node.

    Each row contains:
      - map node properties
      - number of Expertise nodes in the map
      - distinct Lab names linked via Articles
      - distinct SubDomain names linked to the map
    """

    result = session.run(
        """
        MATCH (m:ExpertiseMap)
        OPTIONAL MATCH (lab:Lab {graph_id: m.graph_id})
        OPTIONAL MATCH (e:Expertise)-[:BELONGSTO]->(sd:SubDomain)-[:ISSUBDOMAINOF]->(d:Domain)-[:BELONGSTO]->(m)

        WITH m,
            count(DISTINCT e) AS numExpertises,
            collect(DISTINCT lab.name) AS labs,
            collect(DISTINCT d.name) AS domains,
            collect(DISTINCT sd.name) AS subdomains

        RETURN m, labs, domains, subdomains, numExpertises;
        """
    )

    return [
        {
            "id" : row['m']['graph_id'],
            "name" : row['m']['name'],
            "description" : row['m']['description'],
            "number_of_expertises": row["numExpertises"],
            "labs": row["labs"],
            "domains" : row['domains'],
            "subdomains": row["subdomains"],
        }
        for row in result
    ]


def fetch_graph_by_id(session: Session, graph_id: str) -> dict | None:
    """
    Return full detail for a single ExpertiseMap.

    Returns ``None`` when no ExpertiseMap with the given graph_id exists.
    """

    graph_details = session.run(
        """
        MATCH (m:ExpertiseMap {graph_id: $graph_id})
        OPTIONAL MATCH (lab:Lab {graph_id: m.graph_id})
        OPTIONAL MATCH (en:Entity)-[:BELONGSTO]->(e:Expertise)-[:BELONGSTO]->(sd:SubDomain)-[:ISSUBDOMAINOF]->(d:Domain)-[:BELONGSTO]->(m)

        WITH m,
            count(DISTINCT en) AS numEntities,
            count(DISTINCT e) AS numExpertises,
            collect(DISTINCT lab.name) AS labs,
            collect(DISTINCT d.name) AS domains,
            collect(DISTINCT sd.name) AS subdomains

        RETURN m, labs, domains, subdomains, numExpertises, numEntities;
        """,
        {"graph_id": graph_id}
    ).single()

    if graph_details is None:
        return None

    expertises = session.run("""
        MATCH (m:ExpertiseMap {graph_id: $graph_id})
        MATCH (ex:Expertise {graph_id: m.graph_id})

        OPTIONAL MATCH (ex)-[:BELONGSTO]->(l:Lab)
        OPTIONAL MATCH (e:Entity)-[:BELONGSTO]->(ex)-[:BELONGSTO]->(sd:SubDomain)-[:ISSUBDOMAINOF]->(d:Domain)

        WITH ex,
            collect(DISTINCT l.name) AS labs,
            collect(DISTINCT d.name) AS domains,
            collect(DISTINCT sd.name) AS subdomains,
            count(DISTINCT e) AS size

        RETURN {
            id: ex.id,
            personalized_pagerank_name: ex.personalized_pagerank_name,
            llm_label: ex.llm_label,
            domains: domains,
            labs: labs,
            subdomains: subdomains,
            size : size
        } AS result;
        """,
        {"graph_id": graph_id}    
    )

    
    result = {
        "id" : graph_details['m']['graph_id'],
        "name" : graph_details['m']['name'],
        "description" : graph_details['m']['description'],
        "labs": graph_details["labs"],
        "domains" : graph_details['domains'],
        "entity_count": graph_details["numEntities"],
        "subdomains": graph_details["subdomains"],
    }


    result['expertises'] = [ex['result'] for ex in expertises]

    return result


def graph_exists(session: Session, graph_id: str) -> bool:
    """Return True if an ExpertiseMap with the given graph_id exists."""

    result = session.run(
        "MATCH (m:ExpertiseMap {graph_id: $graph_id}) RETURN count(m) AS c",
        {"graph_id": graph_id},
    )

    return result.single()["c"] > 0


# ── Export ────────────────────────────────────────────────────────────────────

def stream_graph_json(session: Session, graph_id: str) -> str:
    """
    Use APOC streaming export to serialise the subgraph for *graph_id*.

    Returns the complete JSON string.  Nothing is written to disk.
    """
    result = session.run(
        """
        MATCH (n:SubDomain)-[r]->(m)
        WHERE NOT n:Article AND NOT n:Entity and NOT m:Article and NOT m:Entity AND n.graph_id = $graph_id AND m.graph_id = $graph_id
        WITH collect(n) AS sources, collect(r) AS relations, collect(m) AS destinations
        WITH apoc.coll.toSet(sources + destinations) AS allNodes, relations AS allRels
        CALL apoc.export.json.data(allNodes, allRels, null, {stream: true, jsonFormat: 'JSON'})
        YIELD data
        RETURN data
        """,
        {"graph_id": graph_id},
    )
    chunks = [row["data"] for row in result if row["data"]]
    return "".join(chunks)


# ── Visualisation queries ─────────────────────────────────────────────────────

def fetch_taxonomy(session: Session, graph_id: str) -> list[dict]:
    """
    Return Domain → SubDomain relationships for the given graph.

    Each row: {domain_name, subdomain_name, domain_id, subdomain_id}
    """
    result = session.run(
        """
        MATCH p = (sd:SubDomain {graph_id: $graph_id})-[:ISSUBDOMAINOF]->(d:Domain {graph_id: $graph_id})-[:BELONGSTO]->(e:ExpertiseMap {graph_id: $graph_id})

        UNWIND relationships(p) AS r
        WITH p, r, startNode(r) AS src, endNode(r) AS dst

        RETURN collect({
            src: {
                id: src.id,
                name: src.name,
                labels: labels(src),
                llm_label: src.llm_label
            },
            dst: {
                id: dst.id,
                name: dst.name,
                labels: labels(dst),
                llm_label: dst.llm_label
            },
            relation: type(r),
            props: properties(r)
        }) AS triples;
        """,
        {"graph_id": graph_id},
    ).single()

    return result['triples']


def fetch_expertises_graph(
    session: Session, 
    graph_id: str,
    subdomains : Optional[list[str]] = None,
    domains : Optional[list[str]] = None,
    labs : Optional[list[str]] = None
) -> dict:
    """
    Return nodes and edges for the full expertises view:
      Expertise ↔ SubDomain ↔ Domain
    """
    result = session.run(
        f"""        
        MATCH p = (lab:Lab)<-[:BELONGSTO]-(ex:Expertise {{graph_id: $graph_id}})-[:BELONGSTO]->(sd:SubDomain {{graph_id: $graph_id}})
            -[:ISSUBDOMAINOF]->(d:Domain {{graph_id: $graph_id}})
            -[:BELONGSTO]->(e:ExpertiseMap {{graph_id: $graph_id}})

        WHERE true {'AND d.name IN $domains' if domains else ''} {'AND sd.name IN $subdomains' if subdomains else ''} {'AND lab.name IN $labs' if labs else ''}

        UNWIND relationships(p) AS r
        WITH r, startNode(r) AS src, endNode(r) AS dst

        RETURN collect({{
            src: {{
                id: src.id,
                name: src.name,
                labels: labels(src),
                llm_label: src.llm_label,
                personalized_pagerank_name: src.personalized_pagerank_name
            }},
            dst: {{
                id: dst.id,
                name: dst.name,
                labels: labels(dst),
                llm_label: src.llm_label
            }},
            relation: type(r),
            props: properties(r)
        }}) AS triples;
        """,
        {
            "graph_id": graph_id,
            "domains" : domains,
            "subdomains" : subdomains,
            "labs": labs
        },
    ).single()

    return result['triples']


def fetch_expertise_detail(session: Session, graph_id: str, expertise_id: str) -> dict | None:
    """
    Return nodes and edges for a single Expertise:
      Expertise ↔ Entity, Expertise ↔ SubDomain, SubDomain ↔ Domain,
      Entity ↔ SubDomain
    """
    result = session.run(
        """
        MATCH (ex:Expertise {graph_id: $graph_id, id: $expertise_id})

        CALL {
            WITH ex
            MATCH p =
                (en:Entity)-[:BELONGSTO]->(ex)
                -[:BELONGSTO]->(sd:SubDomain {graph_id: $graph_id})
                -[:ISSUBDOMAINOF]->(d:Domain {graph_id: $graph_id})
            UNWIND relationships(p) AS r
            RETURN r

            UNION ALL

            WITH ex
            MATCH p = (ex)<-[:BELONGSTO]-(e1:Entity)
                    -[:HASRELATIONWITH]->(e2:Entity)
                    -[:BELONGSTO]->(ex)
            UNWIND relationships(p) AS r
            RETURN r

            UNION ALL

            WITH ex
            MATCH p = (ex)-[:BELONGSTO]->(:Lab)

            UNWIND relationships(p) AS r
            RETURN r

        }

        WITH r, startNode(r) AS src, endNode(r) AS dst

        RETURN collect({
            src: {
                id: src.id,
                name: src.name,
                labels: labels(src),
                llm_label: src.llm_label,
                personalized_pagerank_name: src.personalized_pagerank_name
            },
            dst: {
                id: dst.id,
                name: dst.name,
                labels: labels(dst),
                llm_label: dst.llm_label,
                personalized_pagerank_name: dst.personalized_pagerank_name
            },
            relation: type(r),
            props: properties(r)
        }) AS triples
        """,
        {
            "graph_id": graph_id,
            "expertise_id": expertise_id
        },
    ).single()

    return result['triples']

def fetch_summary_stats(session: Session, graph_id: str) -> dict:
    """
    Run all 10 summary queries for the given graph and return their results
    as named lists of dicts.
 
    All Cypher is scoped to ``graph_id`` via node properties so multiple
    expertise maps can coexist in the same database.
    """
 
    def _run(cypher: str) -> list[dict]:
        return [dict(row) for row in session.run(cypher, {"graph_id": graph_id})]
 
    # ── Articles ──────────────────────────────────────────────────────────────
 
    articles_by_lab = _run("""
        MATCH (a:Article {graph_id: $graph_id})-[:BELONGSTO]->(l:Lab {graph_id: $graph_id})
        WITH l.name AS lab, count(DISTINCT a.id) AS numArticles
        RETURN lab, numArticles
        ORDER BY numArticles DESC
    """)
 
    articles_by_subdomain = _run("""
        MATCH (a:Article {graph_id: $graph_id})-[:BELONGSTO]->(sd:SubDomain {graph_id: $graph_id})
        WITH sd.name AS sub_domain, count(DISTINCT a.id) AS numArticles
        RETURN sub_domain, numArticles
        ORDER BY numArticles DESC
    """)
 
    articles_by_domain = _run("""
        MATCH (a:Article {graph_id: $graph_id})-[:BELONGSTO]->(sd:SubDomain {graph_id: $graph_id})
              -[:ISSUBDOMAINOF]->(d:Domain {graph_id: $graph_id})
        WITH d.name AS domain, count(DISTINCT a.id) AS numArticles
        RETURN domain, numArticles
        ORDER BY numArticles DESC
    """)
 
    articles_by_domain_lab = _run("""
        MATCH (lab:Lab {graph_id: $graph_id})<-[:BELONGSTO]-(a:Article {graph_id: $graph_id})
              -[:BELONGSTO]->(sd:SubDomain {graph_id: $graph_id})
              -[:ISSUBDOMAINOF]->(d:Domain {graph_id: $graph_id})
        WITH d.name AS domain, lab.name AS lab, count(DISTINCT a.id) AS numArticles
        RETURN lab, domain, numArticles
        ORDER BY lab, domain
    """)
 
    articles_by_subdomain_lab = _run("""
        MATCH (lab:Lab {graph_id: $graph_id})<-[:BELONGSTO]-(a:Article {graph_id: $graph_id})
              -[:BELONGSTO]->(sd:SubDomain {graph_id: $graph_id})
        WITH sd.name AS sub_domain, lab.name AS lab, count(DISTINCT a.id) AS numArticles
        RETURN lab, sub_domain, numArticles
        ORDER BY lab, sub_domain
    """)
 
    # ── Expertises ────────────────────────────────────────────────────────────
 
    expertises_by_lab = _run("""
        MATCH (e:Expertise {graph_id: $graph_id})-[:BELONGSTO]->(l:Lab {graph_id: $graph_id})
        WITH l.name AS lab, count(DISTINCT e.id) AS numExpertises
        RETURN lab, numExpertises
        ORDER BY numExpertises DESC
    """)
 
    expertises_by_subdomain = _run("""
        MATCH (e:Expertise {graph_id: $graph_id})-[:BELONGSTO]->(sd:SubDomain {graph_id: $graph_id})
        WITH sd.name AS sub_domain, count(DISTINCT e.id) AS numExpertises
        RETURN sub_domain, numExpertises
        ORDER BY numExpertises DESC
    """)
 
    expertises_by_domain = _run("""
        MATCH (e:Expertise {graph_id: $graph_id})-[:BELONGSTO]->(sd:SubDomain {graph_id: $graph_id})
              -[:ISSUBDOMAINOF]->(d:Domain {graph_id: $graph_id})
        WITH d.name AS domain, count(DISTINCT e.id) AS numExpertises
        RETURN domain, numExpertises
        ORDER BY numExpertises DESC
    """)
 
    expertises_by_domain_lab = _run("""
        MATCH (lab:Lab {graph_id: $graph_id})<-[:BELONGSTO]-(e:Expertise {graph_id: $graph_id})
              -[:BELONGSTO]->(sd:SubDomain {graph_id: $graph_id})
              -[:ISSUBDOMAINOF]->(d:Domain {graph_id: $graph_id})
        WITH d.name AS domain, lab.name AS lab, count(DISTINCT e.id) AS numExpertises
        RETURN lab, domain, numExpertises
        ORDER BY lab, domain
    """)
 
    expertises_by_subdomain_lab = _run("""
        MATCH (lab:Lab {graph_id: $graph_id})<-[:BELONGSTO]-(e:Expertise {graph_id: $graph_id})
              -[:BELONGSTO]->(sd:SubDomain {graph_id: $graph_id})
        WITH sd.name AS sub_domain, lab.name AS lab, count(DISTINCT e.id) AS numExpertises
        RETURN lab, sub_domain, numExpertises
        ORDER BY lab, sub_domain
    """)
 
    return {
        "articles_by_lab":            articles_by_lab,
        "articles_by_subdomain":      articles_by_subdomain,
        "articles_by_domain":         articles_by_domain,
        "articles_by_domain_lab":     articles_by_domain_lab,
        "articles_by_subdomain_lab":  articles_by_subdomain_lab,
        "expertises_by_lab":          expertises_by_lab,
        "expertises_by_subdomain":    expertises_by_subdomain,
        "expertises_by_domain":       expertises_by_domain,
        "expertises_by_domain_lab":   expertises_by_domain_lab,
        "expertises_by_subdomain_lab": expertises_by_subdomain_lab,
    }
 