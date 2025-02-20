{{- define "apolo-admission-controller-helm-lib.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "apolo-admission-controller-helm-lib.env" -}}
- name: NP_K8S_API_URL
  value: https://kubernetes.default:443
- name: NP_K8S_AUTH_TYPE
  value: token
- name: NP_K8S_CA_PATH
  value: {{ include "apolo-admission-controller-helm-lib.kubeAuthMountRoot" . }}/ca.crt
- name: NP_K8S_TOKEN_PATH
  value: {{ include "apolo-admission-controller-helm-lib.kubeAuthMountRoot" . }}/token
- name: NP_K8S_NS
  value: {{ .Values.namespace | default "default" | quote }}
- name: SERVICE_NAME
  value: "{{ .Values.apoloAdmissionController.serviceName }}"
- name: WEBHOOK_NAME
  value: "{{ .Values.apoloAdmissionController.webhookName }}"
- name: WEBHOOK_PATH
  value: "{{ .Values.apoloAdmissionController.webhookPath }}"
{{- end -}}

{{- define "apolo-admission-controller-helm-lib.kubeAuthMountRoot" -}}
{{- printf "/var/run/secrets/kubernetes.io/serviceaccount" -}}
{{- end -}}
