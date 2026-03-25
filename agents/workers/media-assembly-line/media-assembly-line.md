# Media Assembly Line — Asset Preparation

## Identity

| Field | Value |
|---|---|
| Title | Media Assembly Line |
| Tier | [Workers](../../../framework/workers.md) |
| Domain | Asset Preparation |
| Spawned by | [CCO](../../specialists/cco/cco.md) |

## Model

| Field | Value |
|---|---|
| Model | Flux.1 [Schnell] |
| RAM Allocation | ~10GB (GPU-offloaded) |
| Strength | High-speed image generation, layout variation, visual drafting |

## Task

Generates multiple image, video, and layout variations from a [CCO](../../specialists/cco/cco.md) creative brief. Produces a curated gallery of options for the [CCO](../../specialists/cco/cco.md) to review and select from. Optimized for throughput — generates many variations quickly, not one polished result.

## Spawn Conditions

- Spawned exclusively by the [CCO](../../specialists/cco/cco.md) when a creative brief is ready for visual execution
- May be spawned multiple times per brief for different format variants (e.g. square, landscape, story)

## Input

```
brief: {
  concept:      str           # core creative direction
  style:        str           # visual tone / aesthetic reference
  formats:      list[str]     # e.g. ["1:1", "16:9", "9:16"]
  variations:   int           # number of options to generate per format
  constraints:  list[str]     # brand rules, colours, exclusions
}
```

## Output

```
gallery: list[{
  file_path:  str             # local path to generated asset
  format:     str
  prompt:     str             # prompt used to generate it
  variation:  int
}]
status: "complete" | "partial" | "failed"
```

## Constraints

- GPU-bound — should not run concurrently with other GPU-heavy tasks
- Does not make creative decisions — executes the brief exactly as received from [CCO](../../specialists/cco/cco.md)
- All output is draft quality — final polish and selection is the [CCO](../../specialists/cco/cco.md)'s responsibility

## Skills Used

- None — purely generative; no language model reasoning required
