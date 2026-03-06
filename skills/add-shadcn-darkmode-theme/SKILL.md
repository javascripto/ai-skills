---
name: add-shadcn-darkmode-theme
description: Configuração de dark mode (light/dark/system) para projetos Vite + React + TypeScript com shadcn/ui. Use após a skill add-tailwind-shadcn para criar ThemeProvider, ajustar sonner e validar alternância de tema.
---

# Adicionar Tema shadcn em Vite

## Objetivo
Configurar suporte de tema `light/dark/system` em projetos Vite + React + TypeScript com shadcn/ui, seguindo a documentação oficial de Vite.

## Quando Usar
Use esta skill quando o projeto Vite já estiver com Tailwind + shadcn/ui e você quiser:
- persistência de tema em `localStorage`
- suporte `light/dark/system`
- integração com `sonner`/toaster respeitando tema

Não use esta skill em projetos Next.js.

## Referência Oficial
- Dark mode em Vite: `https://ui.shadcn.com/docs/dark-mode/vite`
- (Fora de escopo) Next.js instalação: `https://ui.shadcn.com/docs/installation/next`
- (Fora de escopo) Next.js dark mode: `https://ui.shadcn.com/docs/dark-mode/next`

## Pré-requisitos
- Projeto Vite + React + TypeScript
- shadcn/ui já inicializado
- alias `@` funcional

## Passos

1. Crie `src/components/theme-provider.tsx`:

```tsx
import { createContext, useContext, useEffect, useState } from "react";

type Theme = "dark" | "light" | "system";

type ThemeProviderProps = {
	children: React.ReactNode;
	defaultTheme?: Theme;
	storageKey?: string;
};

type ThemeProviderState = {
	theme: Theme;
	setTheme: (theme: Theme) => void;
};

const initialState: ThemeProviderState = {
	theme: "system",
	setTheme: () => null,
};

const ThemeProviderContext = createContext<ThemeProviderState>(initialState);

export function ThemeProvider({
	children,
	defaultTheme = "system",
	storageKey = "vite-ui-theme",
	...props
}: ThemeProviderProps) {
	const [theme, setTheme] = useState<Theme>(
		() => (localStorage.getItem(storageKey) as Theme) || defaultTheme
	);

	useEffect(() => {
		const root = window.document.documentElement;

		root.classList.remove("light", "dark");

		if (theme === "system") {
			const systemTheme = window.matchMedia("(prefers-color-scheme: dark)").matches
				? "dark"
				: "light";

			root.classList.add(systemTheme);
			return;
		}

		root.classList.add(theme);
	}, [theme]);

	const value = {
		theme,
		setTheme: (theme: Theme) => {
			localStorage.setItem(storageKey, theme);
			setTheme(theme);
		},
	};

	return (
		<ThemeProviderContext.Provider {...props} value={value}>
			{children}
		</ThemeProviderContext.Provider>
	);
}

export const useTheme = () => {
	const context = useContext(ThemeProviderContext);

	if (context === undefined) {
		throw new Error("useTheme must be used within a ThemeProvider");
	}

	return context;
};
```

2. Ajuste `src/components/ui/sonner.tsx` para usar o hook local:

```tsx
import { useTheme } from "@/components/theme-provider";
```

3. Envolva o app com `ThemeProvider` sem apagar a interface existente (exemplo em `src/App.tsx`):

```tsx
import { ThemeProvider } from "@/components/theme-provider";
import { Button } from "@/components/ui/button";

export default function App() {
	return (
		<ThemeProvider defaultTheme="system" storageKey="vite-ui-theme">
			{/* mantenha aqui o conteúdo original do projeto */}
			<Button>Click me</Button>
		</ThemeProvider>
	);
}
```

Regra: nao substitua a estrutura de telas/rotas do projeto. Apenas adicione o provider envolvendo o conteúdo já existente.

4. Adicione um controle de tema no app como demonstracao, sem destruir a interface original.

Se ainda nao tiver os componentes necessarios, instale:

```bash
npx shadcn@latest add dropdown-menu button --yes
```

Crie `src/components/theme-toggle.tsx`:

```tsx
import { Moon, Sun } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
	DropdownMenu,
	DropdownMenuContent,
	DropdownMenuItem,
	DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { useTheme } from "@/components/theme-provider";

export function ThemeToggle() {
	const { setTheme } = useTheme();

	return (
		<DropdownMenu>
			<DropdownMenuTrigger asChild>
				<Button variant="outline" size="icon">
					<Sun className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
					<Moon className="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
					<span className="sr-only">Toggle theme</span>
				</Button>
			</DropdownMenuTrigger>
			<DropdownMenuContent align="end">
				<DropdownMenuItem onClick={() => setTheme("light")}>Light</DropdownMenuItem>
				<DropdownMenuItem onClick={() => setTheme("dark")}>Dark</DropdownMenuItem>
				<DropdownMenuItem onClick={() => setTheme("system")}>System</DropdownMenuItem>
			</DropdownMenuContent>
		</DropdownMenu>
	);
}
```

Use no app (exemplo de composicao):

```tsx
import { ThemeProvider } from "@/components/theme-provider";
import { ThemeToggle } from "@/components/theme-toggle";

export default function App() {
	return (
		<ThemeProvider defaultTheme="system" storageKey="vite-ui-theme">
			<div className="flex items-center justify-end p-4">
				<ThemeToggle />
			</div>
			{/* mantenha aqui o restante da interface original do projeto */}
		</ThemeProvider>
	);
}
```

Regra: o `ThemeToggle` e para demonstracao/controle de tema. Posicione-o em um header, toolbar ou canto da tela, preservando o layout existente.

## Validação
1. Execute:
```bash
npm run build
```
2. Confirme que compilou sem erro.
3. Se tiver acesso a navegador, rode `npm run dev` e valide troca de tema pelo `ThemeToggle`.

## Checklist Final
- `src/components/theme-provider.tsx` criado.
- `ThemeProvider` aplicado na raiz do app.
- `sonner.tsx` usa `useTheme` de `@/components/theme-provider`.
- `defaultTheme="system"` e `storageKey="vite-ui-theme"` configurados.
- `src/components/theme-toggle.tsx` criado e integrado no app sem remover a UI existente.
- `npm run build` executado com sucesso.

## Iteração
Se houver inconsistência visual entre tema e componentes, revise classes `dark:` e o uso do provider na árvore de componentes.
