import { useEffect, useState } from "react";
import api from "../../api/client";
import Badge from "../../components/Badge";
import Button from "../../components/Button";
import Card from "../../components/Card";
import EmptyState from "../../components/EmptyState";
import Loader from "../../components/Loader";
import Modal from "../../components/Modal";
import { useToast } from "../../contexts/ToastContext";
import { formatDate, getErrorMessage } from "../../utils/formatters";

const blankForm = { name: "", description: "", team_id: "" };

export default function ProjectsPage() {
  const { push } = useToast();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [projects, setProjects] = useState([]);
  const [teams, setTeams] = useState([]);
  const [activity, setActivity] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
  const [form, setForm] = useState(blankForm);
  const [editingId, setEditingId] = useState(null);
  const [isOpen, setIsOpen] = useState(false);

  async function loadData() {
    setLoading(true);
    try {
      const [projectsRes, teamsRes] = await Promise.all([
        api.get("/projects", { params: { page: 1, page_size: 50 } }),
        api.get("/teams"),
      ]);
      setProjects(projectsRes.data);
      setTeams(teamsRes.data);
    } catch (error) {
      push(getErrorMessage(error), "error");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  async function openActivity(project) {
    setSelectedProject(project);
    try {
      const { data } = await api.get(`/projects/${project.id}/activity`);
      setActivity(data);
    } catch (error) {
      push(getErrorMessage(error), "error");
    }
  }

  function openCreate() {
    setForm(blankForm);
    setEditingId(null);
    setIsOpen(true);
  }

  function openEdit(project) {
    setEditingId(project.id);
    setForm({ name: project.name, description: project.description || "", team_id: project.team_id || "" });
    setIsOpen(true);
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setSaving(true);
    try {
      const payload = {
        name: form.name,
        description: form.description || null,
      };
      if (editingId) {
        payload.team_id = form.team_id ? Number(form.team_id) : null;
        await api.put(`/projects/${editingId}`, payload);
        push("Project updated", "success");
      } else {
        await api.post("/projects", payload);
        push("Project created", "success");
      }
      setIsOpen(false);
      await loadData();
    } catch (error) {
      push(getErrorMessage(error), "error");
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete(projectId) {
    if (!window.confirm("Delete this project?")) return;
    try {
      await api.delete(`/projects/${projectId}`);
      push("Project deleted", "success");
      if (selectedProject?.id === projectId) {
        setSelectedProject(null);
        setActivity([]);
      }
      await loadData();
    } catch (error) {
      push(getErrorMessage(error), "error");
    }
  }

  if (loading) return <Loader label="Loading projects..." />;

  return (
    <>
      <div className="grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
        <Card title="Project board" subtitle="Create projects, then attach teams later if required." action={<Button onClick={openCreate}>New Project</Button>}>
          {projects.length ? (
            <div className="space-y-4">
              {projects.map((project) => (
                <div key={project.id} className="rounded-2xl border border-slate-200 p-4">
                  <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                    <button className="text-left" onClick={() => openActivity(project)}>
                      <p className="text-lg font-semibold text-slate-900">{project.name}</p>
                      <p className="mt-1 text-sm text-slate-500">{project.description || "No description provided."}</p>
                    </button>
                    <div className="flex flex-wrap items-center gap-2">
                      <Badge tone={project.team_id ? "info" : "neutral"}>{project.team_id ? `Team #${project.team_id}` : "Personal"}</Badge>
                      <span className="text-xs text-slate-500">{formatDate(project.created_at)}</span>
                    </div>
                  </div>
                  <div className="mt-4 flex gap-2">
                    <Button variant="secondary" onClick={() => openEdit(project)}>Edit</Button>
                    <Button variant="ghost" onClick={() => handleDelete(project.id)}>Delete</Button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <EmptyState title="No projects yet" message="Create your first project. The dashboard will update immediately and the activity timeline will start tracking actions." action={<Button onClick={openCreate}>Create project</Button>} />
          )}
        </Card>

        <Card title={selectedProject ? `Activity · ${selectedProject.name}` : "Project activity timeline"} subtitle="Create, update, and delete actions are tracked here.">
          {selectedProject ? (
            activity.length ? (
              <div className="space-y-4">
                {activity.map((item) => (
                  <div key={item.id} className="relative rounded-2xl border border-slate-200 p-4">
                    <div className="absolute left-4 top-4 h-3 w-3 rounded-full bg-brand-600" />
                    <div className="pl-6">
                      <p className="font-medium text-slate-900">{item.description}</p>
                      <p className="mt-1 text-sm text-slate-500">Action: {item.action}</p>
                      <p className="mt-1 text-xs text-slate-400">{formatDate(item.timestamp)}</p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-slate-500">No activity logged yet.</p>
            )
          ) : (
            <p className="text-sm text-slate-500">Select a project to inspect its activity timeline.</p>
          )}
        </Card>
      </div>

      <Modal open={isOpen} title={editingId ? "Edit project" : "Create project"} onClose={() => setIsOpen(false)}>
        <form className="space-y-4" onSubmit={handleSubmit}>
          <label className="label block">
            Name
            <input className="input" value={form.name} onChange={(e) => setForm((prev) => ({ ...prev, name: e.target.value }))} required />
          </label>
          <label className="label block">
            Description
            <textarea className="input min-h-[110px]" value={form.description} onChange={(e) => setForm((prev) => ({ ...prev, description: e.target.value }))} />
          </label>
          {editingId ? (
            <label className="label block">
              Attach team (optional)
              <select className="input" value={form.team_id} onChange={(e) => setForm((prev) => ({ ...prev, team_id: e.target.value }))}>
                <option value="">No team linked</option>
                {teams.map((team) => (
                  <option key={team.id} value={team.id}>{team.name}</option>
                ))}
              </select>
            </label>
          ) : null}
          <div className="flex justify-end gap-3">
            <Button type="button" variant="secondary" onClick={() => setIsOpen(false)}>Cancel</Button>
            <Button type="submit" disabled={saving}>{saving ? "Saving..." : editingId ? "Save changes" : "Create project"}</Button>
          </div>
        </form>
      </Modal>
    </>
  );
}
