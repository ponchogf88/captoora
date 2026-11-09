import { integer, primaryKey, sqliteTable, text } from "drizzle-orm/sqlite-core";

export const records = sqliteTable("records", {
  owner: text().notNull(),
  id: text().notNull(),
  kind: text().notNull(),
  data: text().notNull(),
  revision: integer().notNull(),
  updated: text().notNull(),
}, (table) => [primaryKey({ columns: [table.owner, table.id] })]);
