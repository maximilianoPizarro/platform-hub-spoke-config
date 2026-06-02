{{/*
  Kairos Community logo (from kairos-operator OLM icon, maximilianoPizarro/kairos).
  Used for all Platform Hub-Spoke ConsoleLink menu icons for a unified look.
*/}}
{{- define "console-links.kairosIconURL" -}}
{{- $svg := .Files.Get "files/kairos-community-icon.svg" | trim -}}
data:image/svg+xml;base64,{{ $svg | b64enc }}
{{- end -}}
