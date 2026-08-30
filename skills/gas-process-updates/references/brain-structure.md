# GAS Knowledge Base (BRAIN) Structure

The `BRAIN/` directory is the central source of truth for the GAS. All paths must be absolute: `${BRAIN_ROOT_PATH}/`.

## Directory Map
- `${BRAIN_ROOT_PATH}/fornitori/`: One `.md` file per supplier using `TEMPLATE_FORNITORE.md`.
- `${BRAIN_ROOT_PATH}/membri/`: 
  - One `.md` file per member using `TEMPLATE_MEMBRO.md`.
  - `REFERENTI.md`: A matrix mapping members to suppliers.
- `${BRAIN_ROOT_PATH}/ordini/`:
  - `correnti.json`: Active orders (Open, Waiting for Delivery, Problems).
  - `storico.json`: Archived list of all past orders.

## Update Rules
1. **Suppliers**: Updates based on email feedback (quality, logistics).
2. **Orders**: New emails triggering status changes must update the JSON first.
3. **Redundancy**: Critical problems must be noted in BOTH `ordini/correnti.json` AND the specific supplier's `.md` file.
