// main.ts — u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee
// entry point (Node 22, stdlib only).
//
// The image is drawn ahead of time by render.py (Pillow) and shipped in
// this repository as entry.png; this program only places a byte-identical
// copy at the output path the grader reads. Deterministic by construction:
// the same input file is copied on every run.
//
// Revision note: the letter's pitch is "come as a guest, not a grader" —
// fast Wi-Fi, real snacks, the good chair, and a couch that has never
// judged anyone — with the printer P.S. as the closing joke and a red wax
// seal (cream star) by the signature. The gate wants exactly 1024x1024
// PNG under 1 MiB; entry.png is 77,364 bytes, verified byte-identical
// across repeated renders.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

function resolveOutDir(): string {
  const fromEnv = process.env.MAKEFUN_OUTPUT_DIR;
  return fromEnv && fromEnv.length > 0 ? fromEnv : "/output";
}

// Copy the pre-rendered invitation letter to the grader's output directory.
const here = dirname(fileURLToPath(import.meta.url));
const outDir = resolveOutDir();
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
