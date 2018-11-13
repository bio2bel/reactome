Command Line Interface
======================
The command line interface allows you to communicate with the package and perform basic functions such as:

* Populate the database: :code:`python3 -m bio2bel_reactome populate`. By default this command populates the database
  only with human information. In order to populate all species pathway information you can add the "--not-only-human"
  argument. By default the database is reset every time is populated. However, another optional parameter
  "--reset-db=False", allows you to avoid the reset. More logging can be activated by added "-vv" or "-v" as an
  argument.

* Drop the database: :code:`python3 -m bio2bel_reactome drop`. More logging can be activated by added "-vv" or "-v" as
  an argument.

* Export gene sets as an excel file: :code:`python3 -m bio2bel_reactome export`. By default, the excel will contain
  all pathways from all species. However, you can add the argument "species" and type the name of a particular one to
  get only those pathways (e.g., "--species='Homo sapiens'""). Since Reactome has a hierarchy pathway structure, you can
  get only the major pathways with the optional parameter "--top-hierarchy".
