{{- define "apolo-admission-controller-helm-lib.postinstallJob" -}}
apiVersion: batch/v1
kind: Job
metadata:
  name: "{{ include "apolo-admission-controller-helm-lib.fullname" . }}-postinstall"
  namespace: "{{ .Values.namespace }}"
  annotations:
    "helm.sh/hook": post-install,post-upgrade
    "helm.sh/hook-delete-policy": hook-succeeded
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: postinstall
          image: ghcr.io/neuro-inc/apolo-admission-controller-lib:latest
          imagePullPolicy: IfNotPresent
          args: ["post-install"]
          env:
            {{- include "platformStorage.env" . | nindent 12 }}
{{- end -}}