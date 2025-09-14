# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

- **Development server**: `pnpm dev` - Starts Next.js dev server on port 3000
- **Build**: `pnpm build` - Creates production build
- **Linting**: `pnpm lint` or `pnpm lint:fix` - ESLint for code quality
- **Formatting**: `pnpm format` or `pnpm format:fix` - Prettier for code formatting
- **Type checking**: `pnpm typecheck` - TypeScript compiler check
- **Full validation**: `pnpm validate` - Runs lint, format, and typecheck together

## Architecture Overview

Agent UI is a Next.js 15 application that provides a modern chat interface for connecting to and interacting with AgentOS instances through the Agno platform.

### Key Architectural Components

**State Management (Zustand)**
- `src/store.ts` - Global state using Zustand with persistence
- Manages endpoint connections, chat messages, agents/teams, sessions, and UI state
- Default endpoint: `http://localhost:7777`

**Core Structure**
- `src/app/page.tsx` - Main layout with Sidebar + ChatArea split view
- `src/components/chat/Sidebar/` - Left sidebar with sessions, agent/team selector, endpoint config
- `src/components/chat/ChatArea/` - Main chat interface with message display and input

**AgentOS Integration**
- `src/api/os.ts` - API functions for connecting to AgentOS instances
- `src/api/routes.ts` - API route definitions
- `src/types/os.ts` - TypeScript definitions for AgentOS data structures

**Message System**
- Supports real-time streaming responses from agents
- Handles tool calls, reasoning steps, and references
- Multi-modal content support (text, images, video, audio)
- Tool call visualization and metrics display

**UI Components**
- Built with shadcn/ui components in `src/components/ui/`
- Custom typography with MarkdownRenderer for agent responses  
- Responsive design using Tailwind CSS
- Theme support via next-themes

### Key Data Flow

1. User selects endpoint and agent/team from sidebar
2. Chat input sends messages via streaming API to AgentOS
3. Real-time responses update global state and render in chat area
4. Sessions are persisted and can be resumed
5. Tool calls, reasoning, and references are displayed inline

## Technology Stack

- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS with shadcn/ui components
- **State**: Zustand with localStorage persistence  
- **Icons**: Lucide React + Radix UI icons
- **Animations**: Framer Motion
- **Package Manager**: pnpm

## File Organization

- `src/app/` - Next.js App Router pages and layout
- `src/components/chat/` - Chat-specific components (Sidebar, ChatArea, Messages)
- `src/components/ui/` - Reusable UI components (shadcn/ui based)
- `src/api/` - AgentOS API integration functions
- `src/hooks/` - Custom React hooks for streaming and chat logic
- `src/lib/` - Utility functions and helpers
- `src/types/` - TypeScript type definitions