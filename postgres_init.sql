CREATE TABLE IF NOT EXISTS items (
  item_no     INT PRIMARY KEY,
  item_name   TEXT NOT NULL,
  category    TEXT CHECK (category IN ('coffee', 'cake')),
  description TEXT,
  price       NUMERIC(8,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS order_items (
  order_no   INT,
  item_no    INT,
  quantity   INT CHECK (quantity > 0),
  order_ts   TIMESTAMP NOT NULL,
  PRIMARY KEY (order_no, item_no),
  FOREIGN KEY (item_no) REFERENCES items(item_no)
);