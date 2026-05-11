CREATE TABLE "lietotaji" (
	"id"	INTEGER,
	"lietotajvards"	TEXT,
	"vards"	TEXT,
	"parole"	TEXT,
	"attels"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);


INSERT INTO "lietotaji" ("lietotajvards", "vards", "parole"
VALUES ('admin', 'Administrators', 'scrypt:32768:8:1$Wkftf0lnDMXs8sFo$d18f1287dab974060578f50439817762ad6bec017f3fed59d68f298bc0f1ec995e794e720b75da9eaf8f7ed93bfd747cf3b9d37392e8e1ab271f6bd333f5d919');
