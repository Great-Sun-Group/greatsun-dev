2024-09-18 21:25:31.309Z: Host information
2024-09-18 21:25:31.309Z: ----------------
2024-09-18 21:25:31.310Z: OS: Ubuntu 22.04.4 LTS (stable release)
2024-09-18 21:25:31.310Z: Image details: https://github.com/github/codespaces-host-images/blob/main/README.md
2024-09-18 21:25:31.310Z: ----------------

=================================================================================
2024-09-18 21:25:31.310Z: Configuration starting...
2024-09-18 21:25:31.352Z: Cloning...

=================================================================================
2024-09-18 21:25:35.823Z: Creating container...
2024-09-18 21:25:35.890Z: $ devcontainer up --id-label Type=codespaces --workspace-folder /var/lib/docker/codespacemount/workspace/greatsun-dev --mount type=bind,source=/.codespaces/agent/mount/cache,target=/vscode --user-data-folder /var/lib/docker/codespacemount/.persistedshare --container-data-folder .vscode-remote/data/Machine --container-system-data-folder /var/vscode-remote --log-level trace --log-format json --update-remote-user-uid-default never --mount-workspace-git-root false --omit-config-remote-env-from-metadata --skip-non-blocking-commands --skip-post-create --config "/var/lib/docker/codespacemount/workspace/greatsun-dev/.devcontainer/devcontainer.json" --override-config /root/.codespaces/shared/merged_devcontainer.json --default-user-env-probe loginInteractiveShell --container-session-data-folder /workspaces/.codespaces/.persistedshare/devcontainers-cli/cache --secrets-file /root/.codespaces/shared/user-secrets-envs.json
2024-09-18 21:25:36.154Z: @devcontainers/cli 0.68.0. Node.js v18.20.4. linux 6.5.0-1025-azure x64.
2024-09-18 21:25:36.795Z: $ docker buildx build --load --build-arg BUILDKIT_INLINE_CACHE=1 -f /tmp/devcontainercli-root/container-features/0.68.0-1726694736787/Dockerfile-with-features -t vsc-greatsun-dev-ab867bc1346698ab1dbffed281a9049b779ac7bb1d994c9884afe4e1a6708841 --target dev_containers_target_stage --build-arg _DEV_CONTAINERS_BASE_IMAGE=dev_container_auto_added_stage_label /var/lib/docker/codespacemount/workspace/greatsun-dev/.devcontainer
2024-09-18 21:25:37.444Z: #0 building with "default" instance using docker driver

#1 [internal] load build definition from Dockerfile-with-features2024-09-18 21:25:37.444Z: 
2024-09-18 21:25:37.862Z: #1 transferring dockerfile: 2.87kB done
2024-09-18 21:25:42.031Z: #1 ...

#2 [internal] load .dockerignore
#2 transferring context: 2B done
#2 DONE 4.7s
2024-09-18 21:25:42.262Z: 
#1 [internal] load build definition from Dockerfile-with-features
2024-09-18 21:25:42.262Z: #1 DONE 4.8s

#3 [internal] load metadata for mcr.microsoft.com/vscode/devcontainers/python:3
2024-09-18 21:25:42.718Z: #3 DONE 0.6s2024-09-18 21:25:42.720Z: 
2024-09-18 21:25:42.838Z: 
#4 [dev_container_auto_added_stage_label 1/3] FROM mcr.microsoft.com/vscode/devcontainers/python:3@sha256:b87bec59ee604de9737b6be24a6b26929e52ce2f70a0042058ce92b01584e456
#4 resolve mcr.microsoft.com/vscode/devcontainers/python:3@sha256:b87bec59ee604de9737b6be24a6b26929e52ce2f70a0042058ce92b01584e456 0.1s done
2024-09-18 21:25:42.964Z: #4 sha256:40c73830d8633c0d3407be022d6ec9a90938f2af9afd484e2ca1ce10f76fa6f1 21.57kB / 21.57kB done
#4 sha256:0de75d8a196e6c1ced48005bbd2f35cfc830d942687aad9224784f701beb1053 3.54kB / 3.54kB done
2024-09-18 21:25:43.163Z: #4 sha256:b87bec59ee604de9737b6be24a6b26929e52ce2f70a0042058ce92b01584e456 1.61kB / 1.61kB done
#4 sha256:8cd46d290033f265db57fd808ac81c444ec5a5b3f189c3d6d85043b647336913 25.17MB / 49.56MB 0.3s
#4 sha256:2e6afa3f266c11e8960349e7866203a9df478a50362bb5488c45fe39d99b2707 0B / 24.05MB 0.3s
#4 sha256:2e66a70da0bec13fb3d492fcdef60fd8a5ef0a1a65c4e8a4909e26742852f0f2 0B / 64.15MB 0.3s
2024-09-18 21:25:43.265Z: #4 sha256:8cd46d290033f265db57fd808ac81c444ec5a5b3f189c3d6d85043b647336913 36.70MB / 49.56MB 0.4s2024-09-18 21:25:43.265Z: 
2024-09-18 21:25:43.265Z: #4 sha256:2e6afa3f266c11e8960349e7866203a9df478a50362bb5488c45fe39d99b2707 15.73MB / 24.05MB 0.4s
2024-09-18 21:25:43.376Z: #4 sha256:8cd46d290033f265db57fd808ac81c444ec5a5b3f189c3d6d85043b647336913 49.05MB / 49.56MB 0.5s2024-09-18 21:25:43.385Z: 
#4 sha256:2e6afa3f266c11e8960349e7866203a9df478a50362bb5488c45fe39d99b2707 24.05MB / 24.05MB 0.5s
#4 sha256:2e66a70da0bec13fb3d492fcdef60fd8a5ef0a1a65c4e8a4909e26742852f0f2 15.73MB / 64.15MB 0.5s
2024-09-18 21:25:43.491Z: #4 sha256:2e66a70da0bec13fb3d492fcdef60fd8a5ef0a1a65c4e8a4909e26742852f0f2 29.36MB / 64.15MB 0.6s
2024-09-18 21:25:43.599Z: #4 sha256:2e66a70da0bec13fb3d492fcdef60fd8a5ef0a1a65c4e8a4909e26742852f0f2 41.17MB / 64.15MB 0.7s
2024-09-18 21:25:43.766Z: #4 sha256:2e66a70da0bec13fb3d492fcdef60fd8a5ef0a1a65c4e8a4909e26742852f0f2 64.15MB / 64.15MB 0.9s
2024-09-18 21:25:48.472Z: #4 sha256:8cd46d290033f265db57fd808ac81c444ec5a5b3f189c3d6d85043b647336913 49.56MB / 49.56MB 5.6s
2024-09-18 21:25:48.664Z: #4 sha256:8cd46d290033f265db57fd808ac81c444ec5a5b3f189c3d6d85043b647336913 49.56MB / 49.56MB 5.7s done2024-09-18 21:25:48.664Z: 
#4 sha256:2e6afa3f266c11e8960349e7866203a9df478a50362bb5488c45fe39d99b2707 24.05MB / 24.05MB 3.9s done
#4 sha256:1c8ff076d818ad6b8557e03e10c83657cc716ab287c8380054ff91571c8cae81 0B / 211.27MB 5.8s
2024-09-18 21:25:48.768Z: #4 sha256:1c8ff076d818ad6b8557e03e10c83657cc716ab287c8380054ff91571c8cae81 11.63MB / 211.27MB 5.9s
2024-09-18 21:25:48.964Z: #4 sha256:2e66a70da0bec13fb3d492fcdef60fd8a5ef0a1a65c4e8a4909e26742852f0f2 64.15MB / 64.15MB 5.8s done
2024-09-18 21:25:48.965Z: #4 sha256:1c8ff076d818ad6b8557e03e10c83657cc716ab287c8380054ff91571c8cae81 44.10MB / 211.27MB 6.1s
#4 extracting sha256:8cd46d290033f265db57fd808ac81c444ec5a5b3f189c3d6d85043b647336913
#4 sha256:76b2d602845c2157857573b7b630d6e22728251609b3a2013b7dfb5604d4a61f 0B / 24.14MB 6.1s
#4 sha256:9d7cafee8af77ad487135151e94ef89c4edcd02ed6fd866d8dbc130a246380d2 0B / 6.16MB 6.1s
2024-09-18 21:25:49.073Z: #4 sha256:1c8ff076d818ad6b8557e03e10c83657cc716ab287c8380054ff91571c8cae81 61.87MB / 211.27MB 6.2s
#4 sha256:76b2d602845c2157857573b7b630d6e22728251609b3a2013b7dfb5604d4a61f 5.24MB / 24.14MB 6.2s
2024-09-18 21:25:49.268Z: #4 sha256:1c8ff076d818ad6b8557e03e10c83657cc716ab287c8380054ff91571c8cae81 77.59MB / 211.27MB 6.4s2024-09-18 21:25:49.269Z: 
#4 sha256:76b2d602845c2157857573b7b630d6e22728251609b3a2013b7dfb5604d4a61f 22.02MB / 24.14MB 6.4s
#4 sha256:9d7cafee8af77ad487135151e94ef89c4edcd02ed6fd866d8dbc130a246380d2 6.16MB / 6.16MB 6.3s done
2024-09-18 21:25:49.369Z: #4 sha256:1c8ff076d818ad6b8557e03e10c83657cc716ab287c8380054ff91571c8cae81 90.99MB / 211.27MB 6.5s2024-09-18 21:25:49.370Z: 
#4 sha256:76b2d602845c2157857573b7b630d6e22728251609b3a2013b7dfb5604d4a61f 24.14MB / 24.14MB 6.5s
#4 sha256:b61bc9b0e1d8628f1588d6d89bfabd6bf871680a211e5cc2803bb77ad8f26170 0B / 250B 6.5s
2024-09-18 21:25:49.545Z: #4 sha256:b61bc9b0e1d8628f1588d6d89bfabd6bf871680a211e5cc2803bb77ad8f26170 250B / 250B 6.6s2024-09-18 21:25:49.545Z: 
2024-09-18 21:25:49.657Z: #4 sha256:1c8ff076d818ad6b8557e03e10c83657cc716ab287c8380054ff91571c8cae81 111.43MB / 211.27MB 6.7s
#4 sha256:76b2d602845c2157857573b7b630d6e22728251609b3a2013b7dfb5604d4a61f 24.14MB / 24.14MB 6.6s done
2024-09-18 21:25:49.776Z: #4 sha256:1c8ff076d818ad6b8557e03e10c83657cc716ab287c8380054ff91571c8cae81 141.56MB / 211.27MB 6.9s2024-09-18 21:25:49.776Z: 
#4 sha256:b61bc9b0e1d8628f1588d6d89bfabd6bf871680a211e5cc2803bb77ad8f26170 250B / 250B 6.7s done
#4 sha256:9d346fcaa81d799fefef3e90e98652c762d0ecf6e46d30fb8bc3c8603a1a8626 5.24MB / 15.28MB 6.9s
#4 sha256:0f91131e0d4ce16d8c791faff8f8c88c3631e2929000267ac7bdb4ed02653c7a 0B / 7.33MB 6.9s
2024-09-18 21:25:49.896Z: #4 sha256:9d346fcaa81d799fefef3e90e98652c762d0ecf6e46d30fb8bc3c8603a1a8626 15.28MB / 15.28MB 7.0s2024-09-18 21:25:49.905Z: 
2024-09-18 21:25:50.056Z: #4 sha256:1c8ff076d818ad6b8557e03e10c83657cc716ab287c8380054ff91571c8cae81 158.89MB / 211.27MB 7.1s
#4 sha256:0f91131e0d4ce16d8c791faff8f8c88c3631e2929000267ac7bdb4ed02653c7a 2.15MB / 7.33MB 7.1s
2024-09-18 21:25:50.160Z: #4 sha256:0f91131e0d4ce16d8c791faff8f8c88c3631e2929000267ac7bdb4ed02653c7a 5.44MB / 7.33MB 7.2s
2024-09-18 21:25:50.266Z: #4 sha256:1c8ff076d818ad6b8557e03e10c83657cc716ab287c8380054ff91571c8cae81 184.55MB / 211.27MB 7.4s2024-09-18 21:25:50.266Z: 
#4 sha256:0f91131e0d4ce16d8c791faff8f8c88c3631e2929000267ac7bdb4ed02653c7a 7.33MB / 7.33MB 7.4s
2024-09-18 21:25:50.563Z: #4 sha256:1c8ff076d818ad6b8557e03e10c83657cc716ab287c8380054ff91571c8cae81 211.27MB / 211.27MB 7.7s2024-09-18 21:25:50.564Z: 
2024-09-18 21:25:52.864Z: #4 extracting sha256:8cd46d290033f265db57fd808ac81c444ec5a5b3f189c3d6d85043b647336913 3.8s done
2024-09-18 21:25:54.865Z: #4 sha256:9d346fcaa81d799fefef3e90e98652c762d0ecf6e46d30fb8bc3c8603a1a8626 15.28MB / 15.28MB 11.8s done2024-09-18 21:25:54.866Z: 
2024-09-18 21:25:54.969Z: #4 sha256:eccef79e7f76ba83b375385276d64f30b432f63dbde71c6535d9b88565b24cb1 0B / 413B 12.1s
2024-09-18 21:25:55.213Z: #4 sha256:0f91131e0d4ce16d8c791faff8f8c88c3631e2929000267ac7bdb4ed02653c7a 7.33MB / 7.33MB 12.1s done
#4 sha256:eccef79e7f76ba83b375385276d64f30b432f63dbde71c6535d9b88565b24cb1 413B / 413B 12.3s
2024-09-18 21:25:55.565Z: #4 sha256:1c8ff076d818ad6b8557e03e10c83657cc716ab287c8380054ff91571c8cae81 211.27MB / 211.27MB 12.7s2024-09-18 21:25:55.565Z: 
2024-09-18 21:25:56.766Z: #4 sha256:1c8ff076d818ad6b8557e03e10c83657cc716ab287c8380054ff91571c8cae81 211.27MB / 211.27MB 13.7s done
2024-09-18 21:25:56.766Z: #4 sha256:3af2c6d1c0fea21a833ea7445a8fc9819d5a50d46194ef81d68743a041974c3a 0B / 135B 13.9s
2024-09-18 21:25:56.887Z: #4 sha256:eccef79e7f76ba83b375385276d64f30b432f63dbde71c6535d9b88565b24cb1 413B / 413B 13.9s done2024-09-18 21:25:56.887Z: 
#4 sha256:3af2c6d1c0fea21a833ea7445a8fc9819d5a50d46194ef81d68743a041974c3a 135B / 135B 14.0s
#4 extracting sha256:2e6afa3f266c11e8960349e7866203a9df478a50362bb5488c45fe39d99b2707 0.1s
#4 sha256:c1196df15577c6381e65d5667bd72ac14585698d7db90f001b157c9177a9da9e 0B / 224B 14.0s
2024-09-18 21:25:56.993Z: #4 sha256:c1196df15577c6381e65d5667bd72ac14585698d7db90f001b157c9177a9da9e 224B / 224B 14.1s
#4 sha256:1bc4809b4744c2cf40d18110e1cbcc53747285893152c6ecbb027096ac04e6a2 0B / 234B 14.1s
2024-09-18 21:25:57.099Z: #4 sha256:3af2c6d1c0fea21a833ea7445a8fc9819d5a50d46194ef81d68743a041974c3a 135B / 135B 14.1s done
#4 sha256:1bc4809b4744c2cf40d18110e1cbcc53747285893152c6ecbb027096ac04e6a2 234B / 234B 14.2s2024-09-18 21:25:57.099Z: 
2024-09-18 21:25:57.200Z: #4 sha256:c1196df15577c6381e65d5667bd72ac14585698d7db90f001b157c9177a9da9e 224B / 224B 14.2s done
#4 sha256:9014ec7eb846799bc0495bcccb733b1991b48369562b52362f54c39f586aefd8 0B / 74.05MB 14.3s
2024-09-18 21:25:57.362Z: #4 sha256:1bc4809b4744c2cf40d18110e1cbcc53747285893152c6ecbb027096ac04e6a2 234B / 234B 14.3s done
#4 sha256:9014ec7eb846799bc0495bcccb733b1991b48369562b52362f54c39f586aefd8 4.19MB / 74.05MB 14.4s
2024-09-18 21:25:57.463Z: #4 sha256:9014ec7eb846799bc0495bcccb733b1991b48369562b52362f54c39f586aefd8 31.30MB / 74.05MB 14.6s
2024-09-18 21:25:57.579Z: #4 sha256:9014ec7eb846799bc0495bcccb733b1991b48369562b52362f54c39f586aefd8 57.67MB / 74.05MB 14.7s
2024-09-18 21:25:57.673Z: #4 sha256:9014ec7eb846799bc0495bcccb733b1991b48369562b52362f54c39f586aefd8 74.05MB / 74.05MB 14.8s
2024-09-18 21:26:01.937Z: #4 extracting sha256:2e6afa3f266c11e8960349e7866203a9df478a50362bb5488c45fe39d99b2707 5.2s
#4 sha256:e02a73e2c357c34aa4b06179163150edc2ec53ef7244cb5a9bba7419d3ad78f7 0B / 2.32MB 19.0s
2024-09-18 21:26:02.147Z: #4 sha256:e02a73e2c357c34aa4b06179163150edc2ec53ef7244cb5a9bba7419d3ad78f7 2.10MB / 2.32MB 19.2s
2024-09-18 21:26:02.259Z: #4 sha256:e02a73e2c357c34aa4b06179163150edc2ec53ef7244cb5a9bba7419d3ad78f7 2.32MB / 2.32MB 19.3s
2024-09-18 21:26:02.485Z: #4 extracting sha256:2e6afa3f266c11e8960349e7866203a9df478a50362bb5488c45fe39d99b2707 5.7s done
2024-09-18 21:26:02.672Z: #4 sha256:9014ec7eb846799bc0495bcccb733b1991b48369562b52362f54c39f586aefd8 74.05MB / 74.05MB 19.8s
2024-09-18 21:26:04.064Z: #4 sha256:9014ec7eb846799bc0495bcccb733b1991b48369562b52362f54c39f586aefd8 74.05MB / 74.05MB 21.1s done
2024-09-18 21:26:04.368Z: #4 sha256:e02a73e2c357c34aa4b06179163150edc2ec53ef7244cb5a9bba7419d3ad78f7 2.32MB / 2.32MB 21.4s done
#4 sha256:35919096fe4e0cd2e67ab8c6d61d7d2aa585733ca03b491e1022486a6c3369c9 12.58MB / 66.52MB 21.5s
#4 sha256:39ab910736846d374dc023e50d556320cd68b5e9efc3a63ed5b9fafb175f8c18 0B / 64.78MB 21.5s
2024-09-18 21:26:04.563Z: #4 sha256:35919096fe4e0cd2e67ab8c6d61d7d2aa585733ca03b491e1022486a6c3369c9 49.48MB / 66.52MB 21.7s
#4 extracting sha256:2e66a70da0bec13fb3d492fcdef60fd8a5ef0a1a65c4e8a4909e26742852f0f2
2024-09-18 21:26:04.667Z: #4 sha256:35919096fe4e0cd2e67ab8c6d61d7d2aa585733ca03b491e1022486a6c3369c9 61.99MB / 66.52MB 21.8s2024-09-18 21:26:04.668Z: 
2024-09-18 21:26:04.772Z: #4 sha256:35919096fe4e0cd2e67ab8c6d61d7d2aa585733ca03b491e1022486a6c3369c9 66.52MB / 66.52MB 21.9s
2024-09-18 21:26:05.447Z: #4 sha256:35919096fe4e0cd2e67ab8c6d61d7d2aa585733ca03b491e1022486a6c3369c9 66.52MB / 66.52MB 22.4s done2024-09-18 21:26:05.447Z: 
2024-09-18 21:26:05.448Z: #4 sha256:39ab910736846d374dc023e50d556320cd68b5e9efc3a63ed5b9fafb175f8c18 3.28MB / 64.78MB 22.5s
2024-09-18 21:26:05.564Z: #4 sha256:39ab910736846d374dc023e50d556320cd68b5e9efc3a63ed5b9fafb175f8c18 33.53MB / 64.78MB 22.7s2024-09-18 21:26:05.564Z: 
2024-09-18 21:26:05.673Z: #4 sha256:39ab910736846d374dc023e50d556320cd68b5e9efc3a63ed5b9fafb175f8c18 54.53MB / 64.78MB 22.8s
2024-09-18 21:26:05.777Z: #4 sha256:39ab910736846d374dc023e50d556320cd68b5e9efc3a63ed5b9fafb175f8c18 64.78MB / 64.78MB 22.9s
2024-09-18 21:26:09.663Z: #4 extracting sha256:2e66a70da0bec13fb3d492fcdef60fd8a5ef0a1a65c4e8a4909e26742852f0f2 5.1s
2024-09-18 21:26:10.881Z: #4 sha256:39ab910736846d374dc023e50d556320cd68b5e9efc3a63ed5b9fafb175f8c18 64.78MB / 64.78MB 27.7s done2024-09-18 21:26:10.882Z: 
2024-09-18 21:26:14.871Z: #4 extracting sha256:2e66a70da0bec13fb3d492fcdef60fd8a5ef0a1a65c4e8a4909e26742852f0f2 10.4s
2024-09-18 21:26:18.307Z: #4 extracting sha256:2e66a70da0bec13fb3d492fcdef60fd8a5ef0a1a65c4e8a4909e26742852f0f2 13.7s done2024-09-18 21:26:18.307Z: 
2024-09-18 21:26:19.830Z: #4 extracting sha256:1c8ff076d818ad6b8557e03e10c83657cc716ab287c8380054ff91571c8cae81
2024-09-18 21:26:24.940Z: #4 extracting sha256:1c8ff076d818ad6b8557e03e10c83657cc716ab287c8380054ff91571c8cae81 5.1s
2024-09-18 21:26:30.221Z: #4 extracting sha256:1c8ff076d818ad6b8557e03e10c83657cc716ab287c8380054ff91571c8cae81 10.4s
2024-09-18 21:26:35.225Z: #4 extracting sha256:1c8ff076d818ad6b8557e03e10c83657cc716ab287c8380054ff91571c8cae81 15.4s2024-09-18 21:26:35.225Z: 
2024-09-18 21:26:40.319Z: #4 extracting sha256:1c8ff076d818ad6b8557e03e10c83657cc716ab287c8380054ff91571c8cae81 20.5s
2024-09-18 21:26:46.521Z: #4 extracting sha256:1c8ff076d818ad6b8557e03e10c83657cc716ab287c8380054ff91571c8cae81 26.7s
2024-09-18 21:26:49.317Z: #4 extracting sha256:1c8ff076d818ad6b8557e03e10c83657cc716ab287c8380054ff91571c8cae81 29.3s done
2024-09-18 21:26:50.922Z: #4 extracting sha256:9d7cafee8af77ad487135151e94ef89c4edcd02ed6fd866d8dbc130a246380d22024-09-18 21:26:50.923Z: 
2024-09-18 21:26:51.525Z: #4 extracting sha256:9d7cafee8af77ad487135151e94ef89c4edcd02ed6fd866d8dbc130a246380d2 0.5s done2024-09-18 21:26:51.525Z: 
2024-09-18 21:26:51.764Z: #4 extracting sha256:76b2d602845c2157857573b7b630d6e22728251609b3a2013b7dfb5604d4a61f
2024-09-18 21:26:55.583Z: #4 extracting sha256:76b2d602845c2157857573b7b630d6e22728251609b3a2013b7dfb5604d4a61f 3.7s done
2024-09-18 21:26:58.217Z: #4 extracting sha256:b61bc9b0e1d8628f1588d6d89bfabd6bf871680a211e5cc2803bb77ad8f261702024-09-18 21:26:58.217Z: 
2024-09-18 21:26:58.366Z: #4 extracting sha256:b61bc9b0e1d8628f1588d6d89bfabd6bf871680a211e5cc2803bb77ad8f26170 done
2024-09-18 21:26:58.418Z: #4 extracting sha256:9d346fcaa81d799fefef3e90e98652c762d0ecf6e46d30fb8bc3c8603a1a86262024-09-18 21:26:58.420Z: 
2024-09-18 21:26:58.982Z: #4 extracting sha256:9d346fcaa81d799fefef3e90e98652c762d0ecf6e46d30fb8bc3c8603a1a8626 0.4s done
2024-09-18 21:26:59.162Z: #4 extracting sha256:0f91131e0d4ce16d8c791faff8f8c88c3631e2929000267ac7bdb4ed02653c7a
2024-09-18 21:27:02.310Z: #4 extracting sha256:0f91131e0d4ce16d8c791faff8f8c88c3631e2929000267ac7bdb4ed02653c7a 3.0s done2024-09-18 21:27:02.310Z: 
2024-09-18 21:27:04.297Z: #4 extracting sha256:eccef79e7f76ba83b375385276d64f30b432f63dbde71c6535d9b88565b24cb1
2024-09-18 21:27:04.440Z: #4 extracting sha256:eccef79e7f76ba83b375385276d64f30b432f63dbde71c6535d9b88565b24cb1 done
2024-09-18 21:27:04.588Z: #4 extracting sha256:3af2c6d1c0fea21a833ea7445a8fc9819d5a50d46194ef81d68743a041974c3a
2024-09-18 21:27:04.737Z: #4 extracting sha256:3af2c6d1c0fea21a833ea7445a8fc9819d5a50d46194ef81d68743a041974c3a done
2024-09-18 21:27:04.758Z: #4 extracting sha256:c1196df15577c6381e65d5667bd72ac14585698d7db90f001b157c9177a9da9e
2024-09-18 21:27:04.909Z: #4 extracting sha256:c1196df15577c6381e65d5667bd72ac14585698d7db90f001b157c9177a9da9e done
2024-09-18 21:27:04.986Z: #4 extracting sha256:1bc4809b4744c2cf40d18110e1cbcc53747285893152c6ecbb027096ac04e6a2
2024-09-18 21:27:05.135Z: #4 extracting sha256:1bc4809b4744c2cf40d18110e1cbcc53747285893152c6ecbb027096ac04e6a2 done
2024-09-18 21:27:05.229Z: #4 extracting sha256:9014ec7eb846799bc0495bcccb733b1991b48369562b52362f54c39f586aefd8
2024-09-18 21:27:10.472Z: #4 extracting sha256:9014ec7eb846799bc0495bcccb733b1991b48369562b52362f54c39f586aefd8 5.2s2024-09-18 21:27:10.472Z: 
2024-09-18 21:27:15.501Z: #4 extracting sha256:9014ec7eb846799bc0495bcccb733b1991b48369562b52362f54c39f586aefd8 10.3s2024-09-18 21:27:15.513Z: 
2024-09-18 21:27:19.276Z: #4 extracting sha256:9014ec7eb846799bc0495bcccb733b1991b48369562b52362f54c39f586aefd8 14.0s done
2024-09-18 21:27:25.175Z: #4 extracting sha256:39ab910736846d374dc023e50d556320cd68b5e9efc3a63ed5b9fafb175f8c18
2024-09-18 21:27:30.795Z: #4 extracting sha256:39ab910736846d374dc023e50d556320cd68b5e9efc3a63ed5b9fafb175f8c18 5.6s2024-09-18 21:27:30.795Z: 
2024-09-18 21:27:31.773Z: #4 extracting sha256:39ab910736846d374dc023e50d556320cd68b5e9efc3a63ed5b9fafb175f8c18 6.6s done
2024-09-18 21:27:33.307Z: #4 extracting sha256:e02a73e2c357c34aa4b06179163150edc2ec53ef7244cb5a9bba7419d3ad78f7
2024-09-18 21:27:33.736Z: #4 extracting sha256:e02a73e2c357c34aa4b06179163150edc2ec53ef7244cb5a9bba7419d3ad78f7 0.3s done
2024-09-18 21:27:33.942Z: #4 extracting sha256:35919096fe4e0cd2e67ab8c6d61d7d2aa585733ca03b491e1022486a6c3369c92024-09-18 21:27:33.942Z: 
2024-09-18 21:27:39.230Z: #4 extracting sha256:35919096fe4e0cd2e67ab8c6d61d7d2aa585733ca03b491e1022486a6c3369c9 5.3s
2024-09-18 21:27:41.994Z: #4 extracting sha256:35919096fe4e0cd2e67ab8c6d61d7d2aa585733ca03b491e1022486a6c3369c9 8.1s done
2024-09-18 21:27:46.222Z: #4 DONE 123.5s
2024-09-18 21:27:46.385Z: 
2024-09-18 21:27:46.385Z: #5 [dev_container_auto_added_stage_label 2/3] RUN apt-get update && export DEBIAN_FRONTEND=noninteractive     && apt-get -y install --no-install-recommends sudo2024-09-18 21:27:46.386Z: 
2024-09-18 21:27:46.764Z: #5 0.533 Get:1 http://deb.debian.org/debian bookworm InRelease [151 kB]
2024-09-18 21:27:46.933Z: #5 0.544 Get:2 http://deb.debian.org/debian bookworm-updates InRelease [55.4 kB]2024-09-18 21:27:46.933Z: 
#5 0.544 Get:3 http://deb.debian.org/debian-security bookworm-security InRelease [48.0 kB]
#5 0.544 Get:4 https://dl.yarnpkg.com/debian stable InRelease [17.1 kB]
#5 0.624 Get:5 http://deb.debian.org/debian bookworm/main amd64 Packages [8787 kB]
#5 0.702 Get:6 http://deb.debian.org/debian bookworm-updates/main amd64 Packages [2468 B]
2024-09-18 21:27:47.080Z: #5 0.775 Get:7 http://deb.debian.org/debian-security bookworm-security/main amd64 Packages [182 kB]
#5 0.849 Get:8 https://dl.yarnpkg.com/debian stable/main all Packages [10.9 kB]2024-09-18 21:27:47.081Z: 
2024-09-18 21:27:47.247Z: #5 0.864 Get:9 https://dl.yarnpkg.com/debian stable/main amd64 Packages [10.9 kB]2024-09-18 21:27:47.247Z: 
2024-09-18 21:27:47.710Z: #5 1.479 Fetched 9265 kB in 1s (9258 kB/s)
#5 1.479 Reading package lists...2024-09-18 21:27:48.091Z: 
2024-09-18 21:27:48.262Z: #5 1.880 Reading package lists...2024-09-18 21:27:48.497Z: 
2024-09-18 21:27:48.605Z: #5 2.278 Building dependency tree...
#5 2.373 Reading state information...2024-09-18 21:27:48.709Z: 
#5 2.478 sudo is already the newest version (1.9.13p3-1+deb12u1).
#5 2.478 0 upgraded, 0 newly installed, 0 to remove and 2 not upgraded.
2024-09-18 21:27:49.061Z: #5 DONE 2.8s2024-09-18 21:27:49.061Z: 
2024-09-18 21:27:49.227Z: 
#6 [dev_container_auto_added_stage_label 3/3] RUN groupadd --gid 1000 vscode     && useradd -s /bin/bash --uid 1000 --gid 1000 -m vscode     && echo vscode ALL=(root) NOPASSWD:ALL > /etc/sudoers.d/vscode     && chmod 0440 /etc/sudoers.d/vscode
2024-09-18 21:27:49.587Z: #6 0.513 groupadd: group 'vscode' already exists
2024-09-18 21:27:49.820Z: #6 ERROR: process "/bin/sh -c groupadd --gid $USER_GID $USERNAME     && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME     && echo $USERNAME ALL=\\(root\\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME     && chmod 0440 /etc/sudoers.d/$USERNAME" did not complete successfully: exit code: 9
2024-09-18 21:27:49.903Z: ------2024-09-18 21:27:49.904Z: 
 > [dev_container_auto_added_stage_label 3/3] RUN groupadd --gid 1000 vscode     && useradd -s /bin/bash --uid 1000 --gid 1000 -m vscode     && echo vscode ALL=(root) NOPASSWD:ALL > /etc/sudoers.d/vscode     && chmod 0440 /etc/sudoers.d/vscode:
0.513 groupadd: group 'vscode' already exists
------
2024-09-18 21:27:49.906Z: Dockerfile-with-features:232024-09-18 21:27:49.907Z: 
--------------------
  22 |     
  23 | >>> RUN groupadd --gid $USER_GID $USERNAME \
  24 | >>>     && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
  25 | >>>     && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
  26 | >>>     && chmod 0440 /etc/sudoers.d/$USERNAME2024-09-18 21:27:49.907Z: 
  27 |     
--------------------
ERROR: failed to solve: process "/bin/sh -c groupadd --gid $USER_GID $USERNAME     && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME     && echo $USERNAME ALL=\\(root\\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME     && chmod 0440 /etc/sudoers.d/$USERNAME" did not complete successfully: exit code: 9
2024-09-18 21:27:49.910Z: Stop: Run: docker buildx build --load --build-arg BUILDKIT_INLINE_CACHE=1 -f /tmp/devcontainercli-root/container-features/0.68.0-1726694736787/Dockerfile-with-features -t vsc-greatsun-dev-ab867bc1346698ab1dbffed281a9049b779ac7bb1d994c9884afe4e1a6708841 --target dev_containers_target_stage --build-arg _DEV_CONTAINERS_BASE_IMAGE=dev_container_auto_added_stage_label /var/lib/docker/codespacemount/workspace/greatsun-dev/.devcontainer
2024-09-18 21:27:49.912Z: Error: Command failed: docker buildx build --load --build-arg BUILDKIT_INLINE_CACHE=1 -f /tmp/devcontainercli-root/container-features/0.68.0-1726694736787/Dockerfile-with-features -t vsc-greatsun-dev-ab867bc1346698ab1dbffed281a9049b779ac7bb1d994c9884afe4e1a6708841 --target dev_containers_target_stage --build-arg _DEV_CONTAINERS_BASE_IMAGE=dev_container_auto_added_stage_label /var/lib/docker/codespacemount/workspace/greatsun-dev/.devcontainer
2024-09-18 21:27:49.912Z:     at FtA (/.codespaces/agent/bin/node_modules/@devcontainers/cli/dist/spec-node/devContainersSpecCLI.js:466:1933)
2024-09-18 21:27:49.912Z:     at process.processTicksAndRejections (node:internal/process/task_queues:95:5)
2024-09-18 21:27:49.913Z:     at async Pm (/.codespaces/agent/bin/node_modules/@devcontainers/cli/dist/spec-node/devContainersSpecCLI.js:465:1896)
2024-09-18 21:27:49.914Z:     at async NH (/.codespaces/agent/bin/node_modules/@devcontainers/cli/dist/spec-node/devContainersSpecCLI.js:465:610)
2024-09-18 21:27:49.914Z:     at async YtA (/.codespaces/agent/bin/node_modules/@devcontainers/cli/dist/spec-node/devContainersSpecCLI.js:482:3771)
2024-09-18 21:27:49.914Z:     at async eB (/.codespaces/agent/bin/node_modules/@devcontainers/cli/dist/spec-node/devContainersSpecCLI.js:482:4886)
2024-09-18 21:27:49.914Z:     at async prA (/.codespaces/agent/bin/node_modules/@devcontainers/cli/dist/spec-node/devContainersSpecCLI.js:663:200)
2024-09-18 21:27:49.915Z:     at async drA (/.codespaces/agent/bin/node_modules/@devcontainers/cli/dist/spec-node/devContainersSpecCLI.js:662:14706)
2024-09-18 21:27:49.915Z: {"outcome":"error","message":"Command failed: docker buildx build --load --build-arg BUILDKIT_INLINE_CACHE=1 -f /tmp/devcontainercli-root/container-features/0.68.0-1726694736787/Dockerfile-with-features -t vsc-greatsun-dev-ab867bc1346698ab1dbffed281a9049b779ac7bb1d994c9884afe4e1a6708841 --target dev_containers_target_stage --build-arg _DEV_CONTAINERS_BASE_IMAGE=dev_container_auto_added_stage_label /var/lib/docker/codespacemount/workspace/greatsun-dev/.devcontainer","description":"An error occurred building the image."}
2024-09-18 21:27:49.923Z: devcontainer process exited with exit code 1

====================================== ERROR ====================================
2024-09-18 21:27:49.956Z: Failed to create container.
=================================================================================
2024-09-18 21:27:49.957Z: Error: Command failed: docker buildx build --load --build-arg BUILDKIT_INLINE_CACHE=1 -f /tmp/devcontainercli-root/container-features/0.68.0-1726694736787/Dockerfile-with-features -t vsc-greatsun-dev-ab867bc1346698ab1dbffed281a9049b779ac7bb1d994c9884afe4e1a6708841 --target dev_containers_target_stage --build-arg _DEV_CONTAINERS_BASE_IMAGE=dev_container_auto_added_stage_label /var/lib/docker/codespacemount/workspace/greatsun-dev/.devcontainer
2024-09-18 21:27:49.957Z: Error code: 1302 (UnifiedContainersErrorFatalCreatingContainer)

====================================== ERROR ====================================
2024-09-18 21:27:49.957Z: Container creation failed.
=================================================================================
2024-09-18 21:27:49.957Z: 

===================================== WARNING ===================================
2024-09-18 21:27:49.958Z: Creating recovery container.
=================================================================================

=================================================================================
2024-09-18 21:28:20.860Z: Creating container...
2024-09-18 21:28:20.893Z: $ devcontainer up --id-label Type=codespaces --workspace-folder /var/lib/docker/codespacemount/workspace/greatsun-dev --mount type=bind,source=/.codespaces/agent/mount/cache,target=/vscode --user-data-folder /var/lib/docker/codespacemount/.persistedshare --container-data-folder .vscode-remote/data/Machine --container-system-data-folder /var/vscode-remote --log-level trace --log-format json --update-remote-user-uid-default never --mount-workspace-git-root false --omit-config-remote-env-from-metadata --skip-non-blocking-commands --skip-post-create --config "/var/lib/docker/codespacemount/workspace/greatsun-dev/.devcontainer/devcontainer.json" --override-config /root/.codespaces/shared/merged_devcontainer.json --default-user-env-probe loginInteractiveShell --container-session-data-folder /workspaces/.codespaces/.persistedshare/devcontainers-cli/cache --secrets-file /root/.codespaces/shared/user-secrets-envs.json
2024-09-18 21:28:21.073Z: @devcontainers/cli 0.68.0. Node.js v18.20.4. linux 6.5.0-1025-azure x64.
2024-09-18 21:28:21.544Z: $alpine -c echo Container started
2024-09-18 21:28:21.564Z: Unable to find image 'mcr.microsoft.com/devcontainers/base:alpine' locally
2024-09-18 21:28:21.725Z: alpine: Pulling from devcontainers/base
2024-09-18 21:28:21.779Z: 
[1A[2K
43c4264eed91: Pulling fs layer 
[1B
[1A[2K
b51add29c49b: 2024-09-18 21:28:21.779Z: Pulling fs layer 
[1B
[1A[2K
657d1e22d76d: Pulling fs layer 
[1B
[1A[2K
99023fc1a298: Pulling fs layer 
[1B
[1A[2K
04a7cffb4d54: Pulling fs layer 
[1B
[1A[2K
a1f3ccc748ed: Pulling fs layer 
[1B
2024-09-18 21:28:21.781Z: [1A[2K
498bd63469f1: Pulling fs layer 
[1B2024-09-18 21:28:21.785Z: [4A2024-09-18 21:28:21.785Z: [2K2024-09-18 21:28:21.785Z: 
2024-09-18 21:28:21.785Z: 99023fc1a298: 2024-09-18 21:28:21.785Z: Waiting 
2024-09-18 21:28:21.785Z: [4B2024-09-18 21:28:21.785Z: [3A2024-09-18 21:28:21.785Z: [2K2024-09-18 21:28:21.785Z: 
2024-09-18 21:28:21.785Z: 04a7cffb4d54: 2024-09-18 21:28:21.785Z: Waiting 
2024-09-18 21:28:21.786Z: [3B2024-09-18 21:28:21.786Z: [2A2024-09-18 21:28:21.786Z: [2K2024-09-18 21:28:21.786Z: 
2024-09-18 21:28:21.786Z: a1f3ccc748ed: 2024-09-18 21:28:21.786Z: Waiting 
2024-09-18 21:28:21.787Z: [2B2024-09-18 21:28:21.787Z: [1A2024-09-18 21:28:21.788Z: [2K2024-09-18 21:28:21.788Z: 
2024-09-18 21:28:21.788Z: 498bd63469f1: 2024-09-18 21:28:21.789Z: Waiting 
2024-09-18 21:28:21.789Z: [1B2024-09-18 21:28:21.859Z: [7A2024-09-18 21:28:21.860Z: [2K
43c4264eed91: Downloading  48.34kB/3.624MB
[7B2024-09-18 21:28:21.876Z: [6A2024-09-18 21:28:21.876Z: [2K2024-09-18 21:28:21.877Z: 
2024-09-18 21:28:21.879Z: b51add29c49b: 2024-09-18 21:28:21.881Z: Download complete 
2024-09-18 21:28:21.883Z: [6B2024-09-18 21:28:21.887Z: [7A2024-09-18 21:28:21.892Z: [2K2024-09-18 21:28:21.893Z: 
2024-09-18 21:28:21.893Z: 43c4264eed91: 2024-09-18 21:28:21.893Z: Downloading  3.624MB/3.624MB
2024-09-18 21:28:21.894Z: [7B2024-09-18 21:28:21.894Z: [7A2024-09-18 21:28:21.894Z: [2K2024-09-18 21:28:21.895Z: 
2024-09-18 21:28:21.895Z: 43c4264eed91: 2024-09-18 21:28:21.897Z: Verifying Checksum 
2024-09-18 21:28:21.897Z: [7B2024-09-18 21:28:21.898Z: [7A2024-09-18 21:28:21.898Z: [2K2024-09-18 21:28:21.898Z: 
2024-09-18 21:28:21.898Z: 43c4264eed91: 2024-09-18 21:28:21.898Z: Download complete 
2024-09-18 21:28:21.898Z: [7B2024-09-18 21:28:21.903Z: [5A[2K
657d1e22d76d: 2024-09-18 21:28:21.903Z: Downloading     134B/134B
[5B[5A[2K
657d1e22d76d: Verifying Checksum 
2024-09-18 21:28:21.907Z: [5B[5A[2K
657d1e22d76d: Download complete 
[5B[7A2024-09-18 21:28:21.908Z: [2K
43c4264eed91: Extracting  65.54kB/3.624MB
[7B2024-09-18 21:28:21.995Z: [4A2024-09-18 21:28:21.999Z: [2K
99023fc1a298: Downloading     223B/223B
[4B[4A[2K
99023fc1a298: Verifying Checksum 
[4B[4A[2K
99023fc1a298: Download complete 
[4B2024-09-18 21:28:22.000Z: [7A[2K
43c4264eed91: Extracting    983kB/3.624MB
[7B2024-09-18 21:28:22.013Z: [3A2024-09-18 21:28:22.013Z: [2K2024-09-18 21:28:22.013Z: 
2024-09-18 21:28:22.013Z: 04a7cffb4d54: 2024-09-18 21:28:22.013Z: Downloading     234B/234B
2024-09-18 21:28:22.013Z: [3B2024-09-18 21:28:22.013Z: [3A2024-09-18 21:28:22.013Z: [2K2024-09-18 21:28:22.013Z: 
2024-09-18 21:28:22.013Z: 04a7cffb4d54: 2024-09-18 21:28:22.013Z: Verifying Checksum 
2024-09-18 21:28:22.014Z: [3B2024-09-18 21:28:22.016Z: [3A2024-09-18 21:28:22.016Z: [2K2024-09-18 21:28:22.016Z: 
2024-09-18 21:28:22.016Z: 04a7cffb4d54: 2024-09-18 21:28:22.016Z: Download complete 
2024-09-18 21:28:22.016Z: [3B2024-09-18 21:28:22.024Z: [2A2024-09-18 21:28:22.024Z: [2K2024-09-18 21:28:22.024Z: 
2024-09-18 21:28:22.024Z: a1f3ccc748ed: 2024-09-18 21:28:22.024Z: Downloading  538.9kB/227.3MB
2024-09-18 21:28:22.024Z: [2B2024-09-18 21:28:22.077Z: [7A2024-09-18 21:28:22.077Z: [2K2024-09-18 21:28:22.077Z: 
2024-09-18 21:28:22.077Z: 43c4264eed91: 2024-09-18 21:28:22.077Z: Extracting  3.624MB/3.624MB
2024-09-18 21:28:22.077Z: [7B2024-09-18 21:28:22.125Z: [2A2024-09-18 21:28:22.125Z: [2K2024-09-18 21:28:22.125Z: 
2024-09-18 21:28:22.125Z: a1f3ccc748ed: 2024-09-18 21:28:22.125Z: Downloading  19.45MB/227.3MB
2024-09-18 21:28:22.125Z: [2B2024-09-18 21:28:22.238Z: [7A2024-09-18 21:28:22.240Z: [2K2024-09-18 21:28:22.241Z: 
2024-09-18 21:28:22.242Z: 43c4264eed91: 2024-09-18 21:28:22.242Z: Pull complete 
2024-09-18 21:28:22.243Z: [7B2024-09-18 21:28:22.243Z: [2A2024-09-18 21:28:22.244Z: [2K2024-09-18 21:28:22.244Z: 
2024-09-18 21:28:22.244Z: a1f3ccc748ed: 2024-09-18 21:28:22.245Z: Downloading  49.73MB/227.3MB
2024-09-18 21:28:22.246Z: [2B2024-09-18 21:28:22.289Z: [6A[2K
b51add29c49b: Extracting     411B/411B
[6B2024-09-18 21:28:22.289Z: [6A[2K
b51add29c49b: Extracting     411B/411B
[6B2024-09-18 21:28:22.326Z: [2A2024-09-18 21:28:22.326Z: [2K
a1f3ccc748ed: Downloading  77.84MB/227.3MB
[2B2024-09-18 21:28:22.458Z: [2A[2K
a1f3ccc748ed: Downloading   97.3MB/227.3MB
[2B2024-09-18 21:28:22.585Z: [2A2024-09-18 21:28:22.585Z: [2K2024-09-18 21:28:22.586Z: 
2024-09-18 21:28:22.586Z: a1f3ccc748ed: 2024-09-18 21:28:22.586Z: Downloading  108.1MB/227.3MB
2024-09-18 21:28:22.586Z: [2B2024-09-18 21:28:22.634Z: [2A2024-09-18 21:28:22.636Z: [2K2024-09-18 21:28:22.637Z: 
2024-09-18 21:28:22.639Z: a1f3ccc748ed: 2024-09-18 21:28:22.645Z: Downloading  121.6MB/227.3MB
2024-09-18 21:28:22.648Z: [2B2024-09-18 21:28:22.736Z: [2A2024-09-18 21:28:22.738Z: [2K2024-09-18 21:28:22.740Z: 
2024-09-18 21:28:22.742Z: a1f3ccc748ed: 2024-09-18 21:28:22.743Z: Downloading  141.6MB/227.3MB
2024-09-18 21:28:22.745Z: [2B2024-09-18 21:28:22.772Z: [1A[2K2024-09-18 21:28:22.774Z: 
2024-09-18 21:28:22.775Z: 498bd63469f1: 2024-09-18 21:28:22.780Z: Downloading  440.6kB/43.37MB
2024-09-18 21:28:22.781Z: [1B2024-09-18 21:28:22.837Z: [2A2024-09-18 21:28:22.838Z: [2K2024-09-18 21:28:22.840Z: 
2024-09-18 21:28:22.841Z: a1f3ccc748ed: 2024-09-18 21:28:22.844Z: Downloading  168.7MB/227.3MB
2024-09-18 21:28:22.849Z: [2B2024-09-18 21:28:22.882Z: [1A2024-09-18 21:28:22.895Z: [2K2024-09-18 21:28:22.895Z: 
2024-09-18 21:28:22.895Z: 498bd63469f1: 2024-09-18 21:28:22.895Z: Downloading  18.14MB/43.37MB
2024-09-18 21:28:22.895Z: [1B2024-09-18 21:28:22.939Z: [2A2024-09-18 21:28:22.942Z: [2K2024-09-18 21:28:22.942Z: 
2024-09-18 21:28:22.942Z: a1f3ccc748ed: 2024-09-18 21:28:22.942Z: Downloading  188.7MB/227.3MB
2024-09-18 21:28:22.942Z: [2B2024-09-18 21:28:22.982Z: [1A2024-09-18 21:28:22.982Z: [2K2024-09-18 21:28:22.983Z: 
2024-09-18 21:28:22.984Z: 498bd63469f1: 2024-09-18 21:28:22.984Z: Downloading  41.14MB/43.37MB
2024-09-18 21:28:22.984Z: [1B2024-09-18 21:28:22.985Z: [1A2024-09-18 21:28:22.987Z: [2K2024-09-18 21:28:22.987Z: 
2024-09-18 21:28:22.988Z: 498bd63469f1: 2024-09-18 21:28:22.988Z: Verifying Checksum 
2024-09-18 21:28:22.989Z: [1B2024-09-18 21:28:22.989Z: [1A2024-09-18 21:28:22.989Z: [2K2024-09-18 21:28:22.990Z: 
2024-09-18 21:28:22.990Z: 498bd63469f1: 2024-09-18 21:28:22.990Z: Download complete 
2024-09-18 21:28:22.991Z: [1B2024-09-18 21:28:23.053Z: [2A2024-09-18 21:28:23.054Z: [2K2024-09-18 21:28:23.054Z: 
2024-09-18 21:28:23.054Z: a1f3ccc748ed: 2024-09-18 21:28:23.054Z: Downloading  210.3MB/227.3MB
2024-09-18 21:28:23.054Z: [2B2024-09-18 21:28:23.096Z: [2A2024-09-18 21:28:23.096Z: [2K
a1f3ccc748ed: Verifying Checksum 
[2B[2A[2K
a1f3ccc748ed: Download complete 
[2B2024-09-18 21:28:24.372Z: [6A[2K
b51add29c49b: Pull complete 
[6B2024-09-18 21:28:24.409Z: [5A[2K
657d1e22d76d: Extracting     134B/134B
[5B2024-09-18 21:28:24.411Z: [5A[2K
657d1e22d76d: Extracting     134B/134B
[5B2024-09-18 21:28:25.893Z: [5A[2K
657d1e22d76d: Pull complete 
[5B2024-09-18 21:28:25.937Z: [4A[2K
99023fc1a298: Extracting     223B/223B
[4B2024-09-18 21:28:25.940Z: [4A[2K
99023fc1a298: Extracting     223B/223B
[4B2024-09-18 21:28:26.106Z: [4A[2K
99023fc1a298: Pull complete 
[4B2024-09-18 21:28:26.134Z: [3A[2K2024-09-18 21:28:26.134Z: 
04a7cffb4d54: Extracting     234B/234B
[3B2024-09-18 21:28:26.135Z: [3A[2K
04a7cffb4d54: Extracting     234B/234B
[3B2024-09-18 21:28:26.263Z: [3A[2K
04a7cffb4d54: Pull complete 
[3B2024-09-18 21:28:26.358Z: [2A[2K
a1f3ccc748ed: Extracting  557.1kB/227.3MB
[2B2024-09-18 21:28:26.465Z: [2A[2K
a1f3ccc748ed: Extracting  3.899MB/227.3MB
[2B2024-09-18 21:28:26.569Z: [2A[2K
a1f3ccc748ed: Extracting  11.14MB/227.3MB
[2B2024-09-18 21:28:26.681Z: [2A[2K
a1f3ccc748ed: Extracting  18.38MB/227.3MB
[2B2024-09-18 21:28:26.792Z: [2A[2K
a1f3ccc748ed: Extracting  21.17MB/227.3MB
[2B2024-09-18 21:28:26.905Z: [2A[2K
a1f3ccc748ed: Extracting  22.28MB/227.3MB
[2B2024-09-18 21:28:27.016Z: [2A[2K
a1f3ccc748ed: Extracting  22.84MB/227.3MB
[2B2024-09-18 21:28:27.187Z: [2A[2K
a1f3ccc748ed: Extracting  23.95MB/227.3MB
[2B2024-09-18 21:28:27.287Z: [2A[2K
a1f3ccc748ed: Extracting  26.74MB/227.3MB
[2B2024-09-18 21:28:27.391Z: [2A[2K
a1f3ccc748ed: Extracting  27.85MB/227.3MB
[2B2024-09-18 21:28:27.496Z: [2A[2K
a1f3ccc748ed: Extracting  31.75MB/227.3MB
[2B2024-09-18 21:28:27.599Z: [2A[2K
a1f3ccc748ed: Extracting  38.44MB/227.3MB
[2B2024-09-18 21:28:27.701Z: [2A[2K
a1f3ccc748ed: Extracting  44.01MB/227.3MB
[2B2024-09-18 21:28:27.807Z: [2A[2K
a1f3ccc748ed: Extracting  49.02MB/227.3MB
[2B2024-09-18 21:28:27.934Z: [2A[2K
a1f3ccc748ed: Extracting  52.36MB/227.3MB
[2B2024-09-18 21:28:28.045Z: [2A[2K
a1f3ccc748ed: Extracting  56.26MB/227.3MB
[2B2024-09-18 21:28:28.150Z: [2A[2K
a1f3ccc748ed: Extracting  59.05MB/227.3MB
[2B2024-09-18 21:28:28.255Z: [2A[2K
a1f3ccc748ed: Extracting   71.3MB/227.3MB
[2B2024-09-18 21:28:28.356Z: [2A[2K
a1f3ccc748ed: Extracting     83MB/227.3MB
[2B2024-09-18 21:28:28.463Z: [2A[2K2024-09-18 21:28:28.464Z: 
a1f3ccc748ed: Extracting  93.03MB/227.3MB
[2B2024-09-18 21:28:28.567Z: [2A[2K2024-09-18 21:28:28.567Z: 
a1f3ccc748ed: Extracting  104.7MB/227.3MB
[2B2024-09-18 21:28:28.712Z: [2A2024-09-18 21:28:28.713Z: [2K
a1f3ccc748ed: Extracting  111.4MB/227.3MB
[2B2024-09-18 21:28:28.815Z: [2A2024-09-18 21:28:28.816Z: [2K
a1f3ccc748ed: Extracting  115.3MB/227.3MB
[2B2024-09-18 21:28:28.948Z: [2A[2K2024-09-18 21:28:28.948Z: 
a1f3ccc748ed: Extracting  117.5MB/227.3MB
[2B2024-09-18 21:28:29.058Z: [2A2024-09-18 21:28:29.058Z: [2K
a1f3ccc748ed: Extracting  119.2MB/227.3MB
[2B2024-09-18 21:28:29.158Z: [2A[2K
a1f3ccc748ed: Extracting    122MB/227.3MB
[2B2024-09-18 21:28:29.263Z: [2A[2K
a1f3ccc748ed: Extracting  128.7MB/227.3MB
[2B2024-09-18 21:28:29.363Z: [2A[2K
a1f3ccc748ed: Extracting  134.8MB/227.3MB
[2B2024-09-18 21:28:29.473Z: [2A[2K
a1f3ccc748ed: Extracting    142MB/227.3MB
[2B2024-09-18 21:28:29.578Z: [2A[2K
a1f3ccc748ed: Extracting  148.2MB/227.3MB
[2B2024-09-18 21:28:29.678Z: [2A[2K
a1f3ccc748ed: Extracting  155.4MB/227.3MB
[2B2024-09-18 21:28:29.782Z: [2A[2K
a1f3ccc748ed: Extracting  161.5MB/227.3MB
[2B2024-09-18 21:28:29.884Z: [2A[2K
a1f3ccc748ed: Extracting  167.1MB/227.3MB
[2B2024-09-18 21:28:29.988Z: [2A[2K
a1f3ccc748ed: Extracting  174.4MB/227.3MB
[2B2024-09-18 21:28:30.088Z: [2A[2K
a1f3ccc748ed: 2024-09-18 21:28:30.090Z: Extracting    181MB/227.3MB
[2B2024-09-18 21:28:30.193Z: [2A2024-09-18 21:28:30.194Z: [2K
a1f3ccc748ed: Extracting  188.3MB/227.3MB
[2B2024-09-18 21:28:30.296Z: [2A[2K
a1f3ccc748ed: Extracting    195MB/227.3MB
[2B2024-09-18 21:28:30.401Z: [2A[2K
a1f3ccc748ed: Extracting  202.2MB/227.3MB
[2B2024-09-18 21:28:30.508Z: [2A[2K
a1f3ccc748ed: Extracting  209.5MB/227.3MB
[2B2024-09-18 21:28:30.613Z: [2A[2K
a1f3ccc748ed: Extracting  216.7MB/227.3MB
[2B2024-09-18 21:28:30.794Z: [2A[2K
a1f3ccc748ed: Extracting  218.9MB/227.3MB
[2B2024-09-18 21:28:30.917Z: [2A[2K
a1f3ccc748ed: Extracting  220.6MB/227.3MB
[2B2024-09-18 21:28:31.028Z: [2A[2K
a1f3ccc748ed: Extracting  222.3MB/227.3MB
[2B2024-09-18 21:28:31.176Z: [2A[2K
a1f3ccc748ed: Extracting  222.8MB/227.3MB
[2B2024-09-18 21:28:31.301Z: [2A[2K
a1f3ccc748ed: Extracting  223.9MB/227.3MB
[2B2024-09-18 21:28:31.693Z: [2A[2K
a1f3ccc748ed: Extracting  224.5MB/227.3MB
[2B2024-09-18 21:28:31.933Z: [2A[2K
a1f3ccc748ed: Extracting  225.1MB/227.3MB
[2B2024-09-18 21:28:32.134Z: [2A2024-09-18 21:28:32.135Z: [2K
a1f3ccc748ed: Extracting  225.6MB/227.3MB
[2B2024-09-18 21:28:32.170Z: [2A2024-09-18 21:28:32.170Z: [2K
a1f3ccc748ed: Extracting  227.3MB/227.3MB
[2B2024-09-18 21:28:36.672Z: [2A[2K
2024-09-18 21:28:36.673Z: a1f3ccc748ed: Pull complete 
[2B2024-09-18 21:28:36.769Z: [1A[2K2024-09-18 21:28:36.769Z: 
498bd63469f1: Extracting  458.8kB/43.37MB
[1B2024-09-18 21:28:36.884Z: [1A[2K
498bd63469f1: Extracting  4.588MB/43.37MB
[1B2024-09-18 21:28:37.009Z: [1A[2K
498bd63469f1: 2024-09-18 21:28:37.009Z: Extracting  5.046MB/43.37MB
[1B2024-09-18 21:28:37.133Z: [1A[2K
498bd63469f1: Extracting  7.799MB/43.37MB
[1B2024-09-18 21:28:37.305Z: [1A[2K
498bd63469f1: Extracting  12.39MB/43.37MB
[1B2024-09-18 21:28:37.418Z: [1A[2K
498bd63469f1: Extracting  12.85MB/43.37MB
[1B2024-09-18 21:28:37.524Z: [1A[2K
498bd63469f1: 2024-09-18 21:28:37.524Z: Extracting  17.43MB/43.37MB
[1B2024-09-18 21:28:37.626Z: [1A[2K2024-09-18 21:28:37.628Z: 
498bd63469f1: Extracting   23.4MB/43.37MB
[1B2024-09-18 21:28:37.744Z: [1A[2K
498bd63469f1: Extracting  28.44MB/43.37MB
[1B2024-09-18 21:28:37.852Z: [1A[2K
498bd63469f1: Extracting  29.36MB/43.37MB
[1B2024-09-18 21:28:37.959Z: [1A[2K
498bd63469f1: Extracting  29.82MB/43.37MB
[1B2024-09-18 21:28:38.102Z: [1A[2K
498bd63469f1: Extracting  30.74MB/43.37MB
[1B2024-09-18 21:28:38.203Z: [1A[2K
498bd63469f1: Extracting   31.2MB/43.37MB
[1B2024-09-18 21:28:38.312Z: [1A[2K
498bd63469f1: Extracting  31.65MB/43.37MB
[1B2024-09-18 21:28:38.454Z: [1A[2K
498bd63469f1: Extracting  33.03MB/43.37MB
[1B2024-09-18 21:28:38.654Z: [1A[2K
498bd63469f1: Extracting  36.24MB/43.37MB
[1B2024-09-18 21:28:38.780Z: [1A[2K
498bd63469f1: Extracting  38.99MB/43.37MB
[1B2024-09-18 21:28:38.885Z: [1A[2K
498bd63469f1: Extracting  39.91MB/43.37MB
[1B2024-09-18 21:28:39.033Z: [1A[2K
498bd63469f1: Extracting  40.83MB/43.37MB
[1B2024-09-18 21:28:39.139Z: [1A[2K
498bd63469f1: Extracting  41.29MB/43.37MB
[1B2024-09-18 21:28:39.157Z: [1A[2K
498bd63469f1: Extracting  43.37MB/43.37MB
[1B2024-09-18 21:28:40.433Z: [1A[2K
498bd63469f1: Pull complete 
[1B2024-09-18 21:28:40.467Z: Digest: sha256:fd42caca3327f072af94d6f5169026fcf95699d9dcfe72552a9a161b67f244722024-09-18 21:28:40.468Z: 
2024-09-18 21:28:40.499Z: Status: Downloaded newer image for mcr.microsoft.com/devcontainers/base:alpine
2024-09-18 21:28:40.823Z: Container started
2024-09-18 21:28:41.078Z: Outcome: success User: vscode WorkspaceFolder: /workspaces/greatsun-dev
2024-09-18 21:28:41.085Z: devcontainer process exited with exit code 0

=================================================================================
2024-09-18 21:28:41.970Z: Running blocking commands...
2024-09-18 21:28:42.014Z: $ devcontainer up --id-label Type=codespaces --workspace-folder /var/lib/docker/codespacemount/workspace/greatsun-dev --mount type=bind,source=/.codespaces/agent/mount/cache,target=/vscode --user-data-folder /var/lib/docker/codespacemount/.persistedshare --container-data-folder .vscode-remote/data/Machine --container-system-data-folder /var/vscode-remote --log-level trace --log-format json --update-remote-user-uid-default never --mount-workspace-git-root false --omit-config-remote-env-from-metadata --skip-non-blocking-commands --expect-existing-container --config "/var/lib/docker/codespacemount/workspace/greatsun-dev/.devcontainer/devcontainer.json" --override-config /root/.codespaces/shared/merged_devcontainer.json --default-user-env-probe loginInteractiveShell --container-session-data-folder /workspaces/.codespaces/.persistedshare/devcontainers-cli/cache --secrets-file /root/.codespaces/shared/user-secrets-envs.json
2024-09-18 21:28:42.280Z: @devcontainers/cli 0.68.0. Node.js v18.20.4. linux 6.5.0-1025-azure x64.
2024-09-18 21:28:42.491Z: Outcome: success User: vscode WorkspaceFolder: /workspaces/greatsun-dev
2024-09-18 21:28:42.501Z: devcontainer process exited with exit code 0

=================================================================================
2024-09-18 21:28:42.550Z: Configuring codespace...

=================================================================================
2024-09-18 21:28:42.550Z: Finished configuring codespace.
