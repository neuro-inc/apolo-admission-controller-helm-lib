{{- define "apolo-admission-controller-helm-lib.preinstallJob" -}}
apiVersion: batch/v1
kind: Job
metadata:
  name: "{{ include "apolo-admission-controller-helm-lib.fullname" . }}-preinstall"
  namespace: "{{ .Values.namespace }}"
  annotations:
    "helm.sh/hook": pre-install,pre-upgrade
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: preinstall
          image: ghcr.io/neuro-inc/apolo-admission-controller-lib:latest
          imagePullPolicy: IfNotPresent
          args: ["pre-install"]
          env:
            {{- include "platformStorage.env" . | nindent 12 }}
{{- end -}}