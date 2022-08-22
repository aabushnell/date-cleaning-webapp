/* CREATE TABLE tl_date_checked (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_string text,
    date_start integer,
    date_end integer,
    country_code text,
    correct integer
);

CREATE TABLE tl_date_manual_mapping (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date text,
    date_start integer,
    date_end integer,
    date_english text,
    date_original text,
    date_original_language text,
    date_match_spatial text,
    comment text,
    url_source text
);

CREATE TABLE tl_dates_countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_string text,
    original_date text,
    mapped_str text,
    date_start integer,
    date_end integer,
    country_strings text,
    date_match_spatial text,
    rank integer
);

CREATE TABLE tl_idai (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_string text,
    date_start integer,
    date_end integer,
    confidence real,
    source text,
    date text,
    country_code text
);

CREATE TABLE tl_synonyms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_string text,
    synonym text,
    comment text
    --country_code text
);


*/

drop table if exists tl_date_checked;
drop table if exists tl_date_manual_mapping;
drop table if exists tl_chrono_cache;
drop table if exists tl_synonyms;
drop table if exists objects;

CREATE TABLE tl_date_checked (
    id integer,
    date_english text,
    location_mapped_country text,
    date_start integer,
    date_end integer,
    correct integer,
    date_match_id text,
    date_match_label text,
    date_match_score real,
    date_match_spatial text,
    date_debug text,
    date_debug_spatial text,
    date_original text,
    collection_id text
);

CREATE TABLE tl_date_manual_mapping (
    id integer,
    input_string text,
    date_start integer,
    date_end integer,
    countries text,
    comment text,
    url_source text,
    is_date_original boolean,
    periodo_id text
);

CREATE TABLE tl_chrono_cache (
    input_string text,
    date_start integer,
    date_end integer,
    date_match_label text,
    date_match_score real,
    date_match_spatial text,
    date_match_id text,
    date_debug text,
    date_debug_spatial text
);

CREATE TABLE tl_synonyms (
    original_string text,
    synonym text,
    comment text,
    country_code text,
    is_date_original boolean
);

CREATE TABLE objects (
    id text,
    date_english text,
    date_debug text,
    date_debug_spatial text,
    date_flags text,
    date_start integer,
    date_end integer,
    location_mapped_country text,
    date_match_label text,
    date_match_score real,
    date_match_id text,
    date_match_spatial text,
    datasource_id text,
    location_original text,
    date_original_lang text,
    url_object_page text,
    object_id text,
    location_debug text,
    attribute_name_english text,
    date_original text
);

drop table if exists tl_date_periodo;
create table tl_date_periodo(
    periodo_id text,
    label text,
    country_list text,
    date_start numeric,
    date_end numeric,
    source text,
    publication_year text
);

insert into objects(id, date_english, date_debug, date_flags, date_start, date_end, location_mapped_country,
                    date_match_id, date_match_label, date_match_score, datasource_id,
                    location_original, date_debug_spatial, date_original_lang, date_match_spatial, url_object_page, object_id,
                    location_debug, attribute_name_english, date_original)
    values("BASJOC-0018773", "date_english", "date_debug", "FF-CH", 1789, 1793, "RU",
                    "periodo:123", "date_match_label", 0.92, "ANTIQ",
                    "FR", "IT", "en", "AU", "google.com", "ANTIQ-123",
                    "the loc debug you want", "description", "fecha original");

insert into objects(id, date_english, date_debug, date_flags, date_start, date_end, location_mapped_country,
                    date_match_id, date_match_label, date_match_score, datasource_id,
                    location_original, date_debug_spatial, date_original_lang, date_match_spatial, url_object_page, object_id,
                    location_debug, attribute_name_english, date_original)
    values("ASDF-123", "about world war 2", "world war 2", "FF-CH", 1800, 1900, "RU",
                    "periodo:123", "world war 2", 1, "ANTIQ",
                    "FR", "IT", "en", "AU", "google.com", "ANTIQ-123",
                    "the loc debug you want", "description", "fecha original");