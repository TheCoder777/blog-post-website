create table if not exists posts (
    id integer primary key autoincrement,
    title text,
    under_title text,
    author text,
    release text,
    content text
);
