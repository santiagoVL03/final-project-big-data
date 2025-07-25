CREATE TABLE comics
(
    id INT,
    title STRING,
    author STRING,
    genre STRING,
    publication_date DATE
) WITH (
    'connector' = 'kafka',
    'topic' = 'new_comics',
    'properties.bootstrap.servers' = '10.147.20.17:9092',
    'properties.group.id' = 'flink_consumer_group',
    'format' = 'json'
);