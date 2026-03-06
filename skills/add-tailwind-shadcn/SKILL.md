---
name: add-tailwind-shadcn
description: Adição de Tailwind CSS v4 e shadcn/ui em projetos Vite + React + TypeScript. Use após a skill init-vite-react-ts para configurar alias @, plugin do Tailwind no Vite, inicialização do shadcn/ui e instalação completa ou mínima de componentes. Não use em projetos Next.js.
---

# Adicionar Tailwind e shadcn/ui

## Objetivo
Configurar Tailwind CSS e shadcn/ui em um projeto Vite + React + TypeScript já existente, deixando o ambiente pronto para desenvolvimento de interface em produção sem sobrescrever o comportamento original do projeto.

## Quando Usar
Use esta skill quando o projeto já tiver sido inicializado com Vite + React + TypeScript e você precisar:
- ativar Tailwind CSS v4
- configurar alias `@` para `src`
- inicializar shadcn/ui
- validar setup com componente `Button`

Para dark mode (light/dark/system), use a skill separada `add-shadcn-theme-vite`.

Não use esta skill em projetos Next.js. Para Next.js, siga a documentação específica de setup para Next.

## Fora de Escopo (Next.js)
Para projetos Next.js, use a documentação oficial do shadcn/ui:
- Instalação no Next.js: `https://ui.shadcn.com/docs/installation/next`
- Dark mode no Next.js: `https://ui.shadcn.com/docs/dark-mode/next`

## Pré-requisitos
- Projeto Vite + React + TypeScript já criado
- Dependências do projeto já instaladas (`npm install`)
- Arquivos padrão do Vite presentes e compilando
- Terminal posicionado no diretório do projeto

## Execução Rápida (comandos)

1. Entre no diretório do projeto.
	 ```bash
	 cd <project-name>
	 ```
	 Motivo: garantir que todos os comandos afetem o projeto correto.

2. Instale Tailwind para Vite.
	 ```bash
	 npm install tailwindcss @tailwindcss/vite
	 ```
	 Motivo: adicionar Tailwind v4 e plugin oficial para integração com Vite.

3. Aplique as edições da seção **Edições Obrigatórias de Arquivo** antes de inicializar o shadcn/ui.
	 Motivo: garantir alias e configuração do Vite prontos para o preflight do shadcn.

4. Instale tipos do Node para resolver `node:path` no `vite.config.ts`.
	 ```bash
	 npm install -D @types/node
	 ```
	 Motivo: evitar erro de tipagem ao usar `path.resolve` no config.

5. Inicialize o shadcn/ui.
	 ```bash
	 npx shadcn@latest init --template vite --base radix --preset vega -y
	 ```
	 Motivo: gerar estrutura base de UI para Vite com a sintaxe compatível da CLI atual.

6. Defina o modo de instalação dos componentes do shadcn/ui.
	 - Se o comando/pedido já disser explicitamente para instalar todos os componentes, execute direto:
	 ```bash
	 npx shadcn@latest add --all --yes
	 ```
	 - Se o comando/pedido não especificar instalação completa, pergunte ao usuário se ele quer instalar todos os componentes.
	 - Se a resposta for "não", execute modo mínimo:
	 ```bash
	 npx shadcn@latest add button --yes
	 ```
	 Motivo: evitar instalação excessiva quando o usuário deseja setup enxuto.

## Edições Obrigatórias de Arquivo

1. Atualize `src/index.css` sem apagar conteúdo útil existente:
	 ```css
	 @import "tailwindcss";
	 ```
	 Motivo: carregar Tailwind CSS v4 pela folha global.
	 Regra: adicione o `@import` no topo do arquivo e mantenha estilos já existentes que sejam necessários para o projeto.

2. Atualize `tsconfig.json` para incluir alias `@/*` (preserve `files` e `references` existentes):
	 ```json
	 {
		 "compilerOptions": {
			 "baseUrl": ".",
			 "paths": {
				 "@/*": ["./src/*"]
			 }
		 }
	 }
	 ```
	 Motivo: permitir resolução de imports com `@/` em tooling e editor.

3. Atualize `tsconfig.app.json` para incluir alias `@/*` em `compilerOptions`:
	 ```json
	 {
		 "compilerOptions": {
			 "baseUrl": ".",
			 "paths": {
				 "@/*": ["./src/*"]
			 }
		 }
	 }
	 ```
	 Motivo: alinhar resolução de módulos no app build do TypeScript.

4. Atualize `vite.config.ts` sem remover configurações existentes:
	 ```ts
	 import path from "node:path";
	 import tailwindcss from "@tailwindcss/vite";
	 import react from "@vitejs/plugin-react";
	 import { defineConfig } from "vite";

	 export default defineConfig({
		 plugins: [react(), tailwindcss()],
		 resolve: {
			 alias: {
				 "@": path.resolve(__dirname, "./src"),
			 },
		 },
	 });
	 ```
	 Motivo: ativar plugin Tailwind e alias `@` no bundler.
	 Regra: preserve plugins, aliases e opções já existentes; apenas adicione `tailwindcss()` e o alias `@` caso não existam.

5. Teste o `Button` sem sobrescrever o fluxo principal do app:

	 Opção recomendada: crie um componente de teste dedicado (ex.: `src/components/ShadcnSmokeTest.tsx`) e renderize no ponto que fizer sentido para o projeto.

	 Modo mínimo (instalou apenas `button`):
	 ```tsx
	 import { Button } from "@/components/ui/button";

	 export default function App() {
		 return (
			 <div className="flex min-h-svh flex-col items-center justify-center">
				 <Button>Click me</Button>
			 </div>
		 );
	 }
	 ```

	 Modo completo (instalou todos os componentes):
	 ```tsx
	 import { Button } from "@/components/ui/button";
	 import { Toaster } from "@/components/ui/sonner";
	 import {
	 	 TooltipProvider,
	 	 Tooltip,
	 	 TooltipContent,
	 	 TooltipTrigger,
	 } from "@/components/ui/tooltip";
	 import { toast } from "sonner";

	 export default function App() {
		 return (
	 	 	 <TooltipProvider delayDuration={0}>
	 	 	 	 <div className="flex min-h-svh flex-col items-center justify-center">
	 	 	 	 	 <Tooltip>
	 	 	 	 	 	 <TooltipTrigger asChild>
	 	 	 	 	 	 	 <Button onClick={() => toast("Componente shadcn funcionando")}>Click me</Button>
	 	 	 	 	 	 </TooltipTrigger>
	 	 	 	 	 	 <TooltipContent>Abrir toaster</TooltipContent>
	 	 	 	 	 </Tooltip>
	 	 	 	 </div>
	 	 	 	 <Toaster />
	 	 	 </TooltipProvider>
		 );
	 }
	 ```
	 Motivo: validar runtime com providers globais e componentes instalados no modo completo.
	 Regra: não remover lógica existente do projeto; incorpore os exemplos como bloco de teste temporário e depois adapte ao layout real.

## Detalhes Obrigatórios
- Preserve configurações existentes nos arquivos (`strict`, `references`, etc.) e adicione apenas o necessário.
- Garanta que o alias `@/*` esteja consistente em `tsconfig.json`, `tsconfig.app.json` e `vite.config.ts`.
- Se o `shadcn init` abrir perguntas interativas, mantenha o alias `@` apontando para `src`.
- O `shadcn init` pode atualizar `src/index.css`; mantenha o carregamento do Tailwind (`@import "tailwindcss"`) junto com as variáveis adicionadas pela ferramenta.
- Não substitua arquivos inteiros quando for possível fazer merge das mudanças.

## Componentes com Configuração Extra
- `tooltip`: para uso amplo no app, envolva o conteúdo do `App.tsx` com `TooltipProvider`.
- `sonner` (toaster): renderize `<Toaster />` na raiz da aplicação para exibir notificações.
- `sidebar`: componentes de sidebar exigem `SidebarProvider`; sem ele ocorre erro de runtime.
- `direction`: use `DirectionProvider` quando precisar controlar direção RTL/LTR global.
- `popover`: não exige configuração global extra; pode ser usado diretamente com `Popover`, `PopoverTrigger` e `PopoverContent`.

## Configuração Global Recomendada
Após instalar os componentes, aplique a configuração base diretamente no componente raiz visual do projeto (geralmente `src/App.tsx`, sem apagar o conteúdo existente) para suportar tooltip e toaster:

Exemplo de composição (adapte ao conteúdo atual do app):

```tsx
import { Button } from "@/components/ui/button";
import { TooltipProvider } from "@/components/ui/tooltip";
import { Toaster } from "@/components/ui/sonner";
import {
	Tooltip,
	TooltipContent,
	TooltipTrigger,
} from "@/components/ui/tooltip";
import { toast } from "sonner";

export default function App() {
	return (
		<TooltipProvider delayDuration={0}>
			{/* mantenha aqui o conteúdo original do projeto */}
			<div className="flex min-h-svh flex-col items-center justify-center">
				<Tooltip>
					<TooltipTrigger asChild>
						<Button onClick={() => toast("Componente shadcn funcionando")}>Click me</Button>
					</TooltipTrigger>
					<TooltipContent>Abrir toaster</TooltipContent>
				</Tooltip>
			</div>
			<Toaster />
		</TooltipProvider>
	);
}

```

Motivo: manter providers de UI no componente de aplicação, sem acoplar `main.tsx` à configuração de componentes e sem perder o comportamento atual do app.

Se o projeto precisar de dark mode (`light/dark/system`), aplique depois a skill `add-shadcn-theme-vite`.

Se usar componentes de sidebar, envolva a área correspondente com `SidebarProvider`.
Se precisar de suporte RTL/LTR global, envolva a aplicação com `DirectionProvider`.

## Validação
1. Execute:
```bash
npm run build
```
2. Confirme que a build finalizou sem erro.
	 Motivo: validar integração de TypeScript, alias e Tailwind no pipeline de produção.

3. Verifique a existência dos arquivos gerados pelo `shadcn init`:
```bash
test -f components.json && test -f src/lib/utils.ts
```
4. Confirme que o comando terminou sem erro.
	 Motivo: garantir que a inicialização do shadcn/ui foi aplicada corretamente.

5. Se tiver acesso a navegador, execute:
```bash
npm run dev
```
6. Verifique se o botão aparece centralizado na tela.
	 Motivo: validar renderização do componente gerado pelo shadcn/ui.

## Checklist Final
- `tailwindcss` e `@tailwindcss/vite` instalados.
- `@types/node` instalado.
- `src/index.css` com `@import "tailwindcss";`.
- Alias `@/*` configurado em `tsconfig.json` e `tsconfig.app.json`.
- `vite.config.ts` com plugin `tailwindcss()` e alias `@`.
- `npx shadcn@latest init --template vite --base radix --preset vega -y` executado.
- Instalação dos componentes realizada conforme escolha do usuário:
	- completa: `npx shadcn@latest add --all --yes`, ou
	- mínima: `npx shadcn@latest add button --yes`.
- `components.json` existe.
- `src/lib/utils.ts` existe.
- Existe um ponto de UI no projeto testando `Button` com Tailwind (sem apagar o conteúdo original).
- `TooltipProvider` e `Toaster` configurados no app base (recomendado).
- Se houver uso de sidebar: `SidebarProvider` configurado.
- Se houver uso de RTL/LTR global: `DirectionProvider` configurado.
- `npm run build` executado com sucesso.
- Se houver acesso a navegador: `npm run dev` executado e validação visual concluída.

## Iteração
Se algum passo falhar, revise os arquivos alterados, corrija conflitos de alias e repita a validação.
