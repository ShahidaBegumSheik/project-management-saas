import { useEffect, useState } from "react";
import Card from "../components/Card";
import { api } from "../api/client";

export default function Projects() {
  const [projects, setProjects] = useState([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [err, setErr] = useState("");
  const [loading, setLoading] = useState(false);

  async function loadProjects() {
    try {
      const res = await api.get("/projects");
      setProjects(res.data);
    } catch (e) {
      setErr(e?.response?.data?.detail || "Could not load projects");
    }
  }

  async function createProject(e) {
    e.preventDefault();
    setErr("");
    setLoading(true);
    try {
      await api.post("/projects", { name, description });
      setName("");
      setDescription("");
      await loadProjects();
    } catch (e) {
      const detail = e?.response?.data?.detail;
      setErr(typeof detail === "string" ? detail : "Could not create project");
    } finally {
      setLoading(false);
    }
  }

  async function removeProject(id) {
    try {
      await api.delete(`/projects/${id}`);
      await loadProjects();
    } catch (e) {
      setErr(e?.response?.data?.detail || "Could not delete project");
    }
  }

  useEffect(() => {
    loadProjects();
  }, []);

  return (
    <div className="grid gap-6 lg:grid-cols-[380px_1fr]">
      <Card title="Create Project" subtitle="Free plan allows up to 3 projects">
        <form onSubmit={createProject} className="space-y-4">
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Project Name</label>
            <input
              className="w-full rounded-xl border px-3 py-2"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Project Alpha"
              required
            />
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Description</label>
            <textarea
              className="min-h-28 w-full rounded-xl border px-3 py-2"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Optional project description"
            />
          </div>

          {err && <div className="rounded-xl bg-red-50 px-3 py-2 text-sm text-red-700">{err}</div>}

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-xl bg-slate-900 px-4 py-2 font-semibold text-white hover:bg-slate-800 disabled:opacity-60"
          >
            {loading ? "Creating..." : "Create Project"}
          </button>
        </form>
      </Card>

      <Card title="My Projects" subtitle="Projects created by the logged-in user">
        {!projects.length ? (
          <p className="text-sm text-slate-500">No projects yet. Create your first one.</p>
        ) : (
          <div className="space-y-4">
            {projects.map((project) => (
              <div key={project.id} className="rounded-2xl border p-4">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <h3 className="text-base font-semibold text-slate-900">{project.name}</h3>
                    <p className="mt-1 text-sm text-slate-600">
                      {project.description || "No description"}
                    </p>
                  </div>
                  <button
                    onClick={() => removeProject(project.id)}
                    className="rounded-lg border px-3 py-2 text-sm text-red-700 hover:bg-red-50"
                  >
                    Delete
                  </button>
                </div>
                <p className="mt-3 text-xs text-slate-400">
                  Project ID: {project.id}
                </p>
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
}
