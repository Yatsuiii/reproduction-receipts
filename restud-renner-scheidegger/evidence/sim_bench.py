"""Run the package's own 2D overreporting simulate() on the deposited checkpoint 4379 with the deposited
shock list, exactly as 2D_simulation_and_error.ipynb cell 2 does, so the output can be compared line by line
with the committed simulation_4379.txt. Writes into the bench clone only."""
import importlib, os, sys, numpy as np, torch, logging
fr = sys.argv[1]  # .../figure_replication/Sec_5_overreporting
sys.path.insert(0, os.path.abspath(os.path.join(fr, '..', '..', 'dptorch')))
os.chdir(fr)
torch.manual_seed(123)
name = "2D_limited_overreporting"
model = importlib.import_module(f"{name}.Model")
ld = lambda i: model.SpecifiedModel.load(path=os.path.abspath(f"data/2D/overreporting/Iter_{i}.pth"),
    cfg_override={"distributed": False, "init_with_zeros": False, "MODEL_NAME": name})
m, m_prev = ld(4379), ld(4378)
shock = np.loadtxt("data/2D/overreporting/2D_or_shock_lst.txt")
logging.getLogger("DPGPModel").setLevel(30)
pp = importlib.import_module(f"{name}.PostProcess")
os.makedirs("/home/claude/bench_out", exist_ok=True); os.chdir("/home/claude/bench_out")
pp.simulate(m, m_prev, m.cfg, model, shock)
