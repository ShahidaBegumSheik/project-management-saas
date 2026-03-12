import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import api from "../../api/client";
import Badge from "../../components/Badge";
import Button from "../../components/Button";
import Card from "../../components/Card";
import EmptyState from "../../components/EmptyState";
import Loader from "../../components/Loader";
import Modal from "../../components/Modal";
import { useToast } from "../../contexts/ToastContext";
import { formatDate, getErrorMessage } from "../../utils/formatters";


export default function TeamsPage() {
  const { push } = useToast();
  const [searchParams, setSearchParams] = useSearchParams();


  const inviteToken = searchParams.get("inviteToken");


  const [loading, setLoading] = useState(true);
  const [teams, setTeams] = useState([]);
  const [projects, setProjects] = useState([]);
  const [selectedTeam, setSelectedTeam] = useState(null);
  const [detail, setDetail] = useState(null);


  const [teamModal, setTeamModal] = useState(false);
  const [inviteModal, setInviteModal] = useState(false);


  const [teamForm, setTeamForm] = useState({
    name: "",
    description: "",
    project_id: "",
  });


  const [inviteForm, setInviteForm] = useState({ email: "" });
  const [saving, setSaving] = useState(false);
  const [responding, setResponding] = useState(false);


  async function loadAll(preferredTeamId = null) {
    setLoading(true);
    try {
      const [teamsRes, projectsRes] = await Promise.all([
        api.get("/teams"),
        api.get("/projects", { params: { page: 1, page_size: 100 } }),
      ]);


      const teamsData = teamsRes.data || [];
      const projectsData = projectsRes.data || [];


      setTeams(teamsData);
      setProjects(projectsData);


      if (!teamsData.length) {
        setSelectedTeam(null);
        setDetail(null);
        return;
      }


      const teamIdToLoad =
        preferredTeamId ||
        selectedTeam?.id ||
        teamsData[0]?.id;


      await loadDetail(teamIdToLoad);
    } catch (error) {
      push(getErrorMessage(error), "error");
    } finally {
      setLoading(false);
    }
  }


  async function loadDetail(teamId) {
    try {
      const { data } = await api.get(`/teams/${teamId}`);
      setSelectedTeam(data.team);
      setDetail(data);
    } catch (error) {
      push(getErrorMessage(error), "error");
    }
  }


  useEffect(() => {
    loadAll();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);


  async function createTeam(event) {
    event.preventDefault();
    setSaving(true);


    try {
      const payload = {
        ...teamForm,
        project_id: Number(teamForm.project_id),
      };


      const res = await api.post("/teams", payload);


      push("Team created", "success");
      setTeamModal(false);
      setTeamForm({ name: "", description: "", project_id: "" });


      await loadAll(res.data?.id);
    } catch (error) {
      push(getErrorMessage(error), "error");
    } finally {
      setSaving(false);
    }
  }


  async function sendInvite(event) {
    event.preventDefault();
    if (!selectedTeam) return;


    setSaving(true);


    try {
      await api.post(`/teams/${selectedTeam.id}/invite`, inviteForm);
      push("Invitation sent", "success");
      setInviteModal(false);
      setInviteForm({ email: "" });
      await loadDetail(selectedTeam.id);
    } catch (error) {
      push(getErrorMessage(error), "error");
    } finally {
      setSaving(false);
    }
  }


  async function respondToInvitation(action) {
    if (!inviteToken) return;


    setResponding(true);
    try {
      await api.post(`/teams/invitations/${inviteToken}`, { action });


      push(
        action === "accept"
          ? "Invitation accepted successfully"
          : "Invitation declined successfully",
        "success"
      );


      searchParams.delete("inviteToken");
      setSearchParams(searchParams);


      await loadAll();
    } catch (error) {
      push(getErrorMessage(error), "error");
    } finally {
      setResponding(false);
    }
  }


  if (loading) {
    return <Loader label="Loading teams..." />;
  }


  return (
    <div className="space-y-6">
      {inviteToken ? (
        <Card
          title="Pending invitation detected"
          subtitle="You opened the user panel with a team invitation token."
        >
          <div className="flex flex-wrap gap-3">
            <Button
              onClick={() => respondToInvitation("accept")}
              disabled={responding}
            >
              {responding ? "Processing..." : "Accept invitation"}
            </Button>


            <Button
              variant="secondary"
              onClick={() => respondToInvitation("decline")}
              disabled={responding}
            >
              {responding ? "Processing..." : "Decline invitation"}
            </Button>
          </div>
        </Card>
      ) : null}


      <div className="grid gap-6 xl:grid-cols-[0.95fr_1.05fr]">
        <Card
          title="Your teams"
          subtitle="Each team must be associated with a project."
          action={<Button onClick={() => setTeamModal(true)}>Create team</Button>}
        >
          {teams.length ? (
            <div className="space-y-3">
              {teams.map((team) => (
                <button
                  key={team.id}
                  type="button"
                  className={`w-full rounded-2xl border p-4 text-left transition ${
                    selectedTeam?.id === team.id
                      ? "border-blue-300 bg-blue-50"
                      : "border-slate-200 bg-white hover:bg-slate-50"
                  }`}
                  onClick={() => loadDetail(team.id)}
                >
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <p className="font-semibold text-slate-900">{team.name}</p>
                      <p className="mt-1 text-sm text-slate-500">
                        {team.description || "No description"}
                      </p>
                    </div>
                    <span className="text-xs text-slate-500">
                      {formatDate(team.created_at)}
                    </span>
                  </div>
                </button>
              ))}
            </div>
          ) : (
            <EmptyState
              title="No teams yet"
              message="Create a team for one of your existing projects to start collaboration."
              action={<Button onClick={() => setTeamModal(true)}>Create team</Button>}
            />
          )}
        </Card>


        <Card
          title={selectedTeam ? selectedTeam.name : "Team detail"}
          subtitle={
            selectedTeam
              ? "Review members, linked projects, and invitation history."
              : "Select a team to inspect details."
          }
          action={
            selectedTeam ? (
              <Button onClick={() => setInviteModal(true)}>Invite member</Button>
            ) : null
          }
        >
          {detail ? (
            <div className="space-y-6">
              <section>
                <h4 className="mb-3 font-semibold text-slate-900">Members</h4>
                <div className="space-y-2">
                  {detail.members?.length ? (
                    detail.members.map((member) => (
                      <div
                        key={member.user_id}
                        className="flex items-center justify-between rounded-2xl border border-slate-200 px-4 py-3"
                      >
                        <div>
                          <p className="font-medium text-slate-900">{member.email}</p>
                          <p className="text-sm text-slate-500">
                            User #{member.user_id}
                          </p>
                        </div>
                        <Badge tone={member.role === "owner" ? "info" : "neutral"}>
                          {member.role}
                        </Badge>
                      </div>
                    ))
                  ) : (
                    <p className="text-sm text-slate-500">No members found.</p>
                  )}
                </div>
              </section>


              <section>
                <h4 className="mb-3 font-semibold text-slate-900">Team projects</h4>
                <div className="space-y-2">
                  {detail.projects?.length ? (
                    detail.projects.map((project) => (
                      <div
                        key={project.id}
                        className="rounded-2xl border border-slate-200 px-4 py-3"
                      >
                        <p className="font-medium text-slate-900">{project.name}</p>
                        <p className="text-sm text-slate-500">
                          {project.description || "No description"}
                        </p>
                      </div>
                    ))
                  ) : (
                    <p className="text-sm text-slate-500">No project linked yet.</p>
                  )}
                </div>
              </section>


              <section>
                <h4 className="mb-3 font-semibold text-slate-900">
                  Invitation history
                </h4>
                <div className="space-y-2">
                  {detail.invitations?.length ? (
                    detail.invitations.map((invitation) => (
                      <div
                        key={invitation.id}
                        className="flex items-center justify-between rounded-2xl border border-slate-200 px-4 py-3"
                      >
                        <p className="text-sm text-slate-700">
                          {invitation.invited_email}
                        </p>
                        <p className="text-xs text-slate-500">
                          Invited on {formatDate(invitation.invited_at)}
                        </p>
                        <Badge
                          tone={
                            invitation.status === "accepted"
                              ? "success"
                              : invitation.status === "declined"
                              ? "danger"
                              : "warning"
                          }
                        >
                          {invitation.status}
                        </Badge>
                      </div>
                    ))
                  ) : (
                    <p className="text-sm text-slate-500">
                      No invitations sent yet.
                    </p>
                  )}
                </div>
              </section>
            </div>
          ) : (
            <p className="text-sm text-slate-500">
              Select a team to review its members, linked project, and invitations.
            </p>
          )}
        </Card>
      </div>


      <Modal
        open={teamModal}
        title="Create project team"
        onClose={() => setTeamModal(false)}
      >
        <form className="space-y-4" onSubmit={createTeam}>
          <label className="label block">
            Team name
            <input
              className="input"
              value={teamForm.name}
              onChange={(e) =>
                setTeamForm((prev) => ({ ...prev, name: e.target.value }))
              }
              required
            />
          </label>


          <label className="label block">
            Description
            <textarea
              className="input min-h-[90px]"
              value={teamForm.description}
              onChange={(e) =>
                setTeamForm((prev) => ({ ...prev, description: e.target.value }))
              }
            />
          </label>


          <label className="label block">
            Project
            <select
              className="input"
              value={teamForm.project_id}
              onChange={(e) =>
                setTeamForm((prev) => ({ ...prev, project_id: e.target.value }))
              }
              required
            >
              <option value="">Select a project</option>
              {projects
                .filter((project) => !project.team_id)
                .map((project) => (
                  <option key={project.id} value={project.id}>
                    {project.name}
                  </option>
                ))}
            </select>
          </label>


          <div className="flex justify-end gap-3">
            <Button
              type="button"
              variant="secondary"
              onClick={() => setTeamModal(false)}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={saving}>
              {saving ? "Creating..." : "Create team"}
            </Button>
          </div>
        </form>
      </Modal>


      <Modal
        open={inviteModal}
        title="Invite member"
        onClose={() => setInviteModal(false)}
      >
        <form className="space-y-4" onSubmit={sendInvite}>
          <label className="label block">
            User email
            <input
              className="input"
              type="email"
              value={inviteForm.email}
              onChange={(e) => setInviteForm({ email: e.target.value })}
              required
            />
          </label>


          <div className="flex justify-end gap-3">
            <Button
              type="button"
              variant="secondary"
              onClick={() => setInviteModal(false)}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={saving}>
              {saving ? "Sending..." : "Send invitation"}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
}