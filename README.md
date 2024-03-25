# Apache Arrow

- [arrow.apache.org](https://arrow.apache.org/)
  - [github](https://github.com/apache/arrow)
  - [docs](https://arrow.apache.org/docs/)
  - [install](https://arrow.apache.org/install/)

## Developing inside a Container

- [containers.dev](https://containers.dev/)
  - [reference](https://containers.dev/implementors/json_reference/)
- github: [devcontainers](https://github.com/devcontainers)
  - [images](https://github.com/devcontainers/images)
  - [features](https://github.com/devcontainers/features)
- vscode
  - docs: [Developing inside a Container](https://code.visualstudio.com/docs/devcontainers/containers)

### Launch the container

Launch a Apache Arrow development environment:

1. Start VS Code
2. Open **Command Palette** with `F1`
3. Run: **Dev Containers: Open Folder in Container...**

### Hello World

- python: [Hello World](python/helloworld/README.md)

```bash
cd /workspace/python/helloworld
python -m helloworld
```

### Attach to Hadoop Nodes

```bash
docker exec -it apache-arrow_devcontainer-namenode-1 bash
docker exec -it apache-arrow_devcontainer-datanode-1 bash
```

```bash
hdfs dfs -ls -R /

drwxr-xr-x   - vscode supergroup          0 2024-03-25 02:59 /user
drwxr-xr-x   - vscode supergroup          0 2024-03-25 02:59 /user/vscode
-rw-r--r--   3 vscode supergroup       1247 2024-03-25 02:59 /user/vscode/birthdays.parquet
drwxr-xr-x   - vscode supergroup          0 2024-03-25 02:59 /user/vscode/output
-rw-r--r--   3 vscode supergroup       1207 2024-03-25 02:59 /user/vscode/output/0.parquet
-rw-r--r--   3 vscode supergroup       1207 2024-03-25 02:59 /user/vscode/output/1.parquet
-rw-r--r--   3 vscode supergroup       1207 2024-03-25 02:59 /user/vscode/output/2.parquet
``
