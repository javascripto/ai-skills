---
name: init-vite-react-ts
description: Inicialização automatizada de projetos Vite com React e TypeScript. Use para criar um novo projeto frontend com Vite, React e TypeScript, realizando todos os passos de limpeza e configuração inicial.
---

# Inicializar Projeto Vite React TypeScript

## Objetivo
Criar um projeto frontend limpo usando Vite, React e TypeScript, sem interação manual.

## Quando Usar
Sempre que for necessário iniciar um novo projeto frontend com:
- React
- TypeScript
- Vite

## Pré-requisitos
- Node.js LTS instalado
- npm disponível
- Terminal Unix-like

## Execução Rápida (comandos)

1. Crie o projeto:
   ```bash
   npm create vite@latest <project-name> -- --template react-ts --no-interactive --no-rolldown
   ```
   Motivo: gera a base oficial React + TypeScript do Vite de forma reproduzível.
2. Entre na pasta e instale dependências:
   ```bash
   cd <project-name>
   npm install
   ```
   Motivo: instala as dependências necessárias para build e execução local.
3. Inicialize git no projeto gerado:
   ```bash
   git init
   ```
   Motivo: prepara versionamento desde o primeiro commit do projeto.
4. Remova arquivos do template padrão:
   ```bash
   rm -f public/vite.svg src/assets/react.svg src/App.css
   ```
   Motivo: elimina arquivos de exemplo para começar com uma base limpa.
5. Copie o favicon de referência para o projeto:
   ```bash
   cp <path-da-skill>/references/favicon.ico public/favicon.ico
   ```
   Motivo: garante identidade visual mínima e evita referência quebrada ao favicon padrão.

## Edições Obrigatórias de Arquivo

1. Substitua `src/App.tsx` por:
   ```tsx
   export default function App() {
     return <h1>Projeto <project-name> iniciado</h1>;
   }
   ```
    Motivo: remove UI de exemplo e deixa um ponto inicial explícito do projeto.

2. Substitua `src/index.css` por:
   ```css
   /* arquivo limpo intencionalmente */
   ```
   Motivo: evita herdar estilos globais do template padrão.

3. Substitua `src/main.tsx` por:
   ```tsx
   import { createRoot } from "react-dom/client";
   import App from "./App.tsx";
   import "./index.css";

   const rootElement = document.getElementById("root") as HTMLElement;
   if (!rootElement) throw new Error("Root element not found");

   createRoot(rootElement).render(<App />);
   ```
   Motivo: simplifica o bootstrap (sem `StrictMode`) e evita erro silencioso quando `#root` não existe.

4. Atualize `index.html` com estes requisitos:
   - Use `<html translate="no">` (sem `lang`).
   - Defina o título como nome do projeto.
   - Garanta a meta viewport:
     ```html
     <meta
       name="viewport"
       content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"
     />
     ```
   - Aponte o favicon para `/favicon.ico`:
     ```html
     <link rel="icon" type="image/x-icon" href="/favicon.ico" />
     ```
    Motivo: padroniza internacionalização, responsividade e metadados mínimos de carregamento.

## Detalhes Obrigatórios
- Remova qualquer import/referência a arquivos apagados (`vite.svg`, `react.svg`, `App.css`).
- Não use `StrictMode` no `src/main.tsx`.
- Garanta que `public/favicon.ico` exista antes da validação. Ele deve ser copiado de `references/favicon.ico`.
- O arquivo `references/favicon.svg` é apenas referência para gerar um novo ícone/base64, se necessário.

## Validação
1. Execute:
```bash
npm run build
```
2. Confirme que a build finalizou sem erro.
   Motivo: valida compilação de produção e detecta erros de TypeScript/import cedo.
3. Execute:
```bash
git rev-parse --is-inside-work-tree
```
4. Confirme que o comando retornou `true`.
   Motivo: garante que o versionamento Git foi inicializado corretamente.
5. Se tiver acesso a navegador, execute:
```bash
npm run dev
```
6. Verifique no navegador se a página abriu sem erros.
   Motivo: valida comportamento em runtime e renderização no ambiente de desenvolvimento.

## Checklist Final
- versionamento git inicializado.
- `src/App.tsx` atualizado.
- `src/index.css` limpo.
- `src/main.tsx` sem `StrictMode`, com `rootElement` validado.
- `index.html` com `translate="no"`, viewport, título correto e favicon `/favicon.ico`.
- `public/favicon.ico` presente.
- `npm run build` executado com sucesso.
- `git rev-parse --is-inside-work-tree` retornou `true`.
- Se houver acesso a navegador: `npm run dev` executado e validação visual concluída.

## Iteração
Se algum passo falhar, revise os arquivos conforme as instruções acima e ajuste o SKILL.md ou scripts conforme necessário.
