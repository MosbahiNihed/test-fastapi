FROM liquibase/liquibase:4.29

# Changelogs are baked into the image so it can run anywhere (CI, Kubernetes Job, ...)
COPY changelog /liquibase/changelog

# Connection details (URL, username, password) are supplied at runtime via
# LIQUIBASE_COMMAND_URL / LIQUIBASE_COMMAND_USERNAME / LIQUIBASE_COMMAND_PASSWORD.
ENV LIQUIBASE_SEARCH_PATH=/liquibase/changelog \
    LIQUIBASE_COMMAND_CHANGELOG_FILE=db.changelog-master.yaml \
    LIQUIBASE_COMMAND_CONTEXTS=dev

CMD ["update"]
