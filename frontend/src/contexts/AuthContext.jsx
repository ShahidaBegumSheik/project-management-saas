import { createContext, useContext, useEffect, useMemo, useState } from "react";
import api, {
  clearAuthSession,
  getStoredUser,
  getToken,
  setAuthSession,
} from "../api/client";


const AuthContext = createContext(null);


export function AuthProvider({ children }) {
  const [token, setToken] = useState(getToken());
  const [user, setUser] = useState(getStoredUser());
  const [loading, setLoading] = useState(true);


  useEffect(() => {
    async function bootstrap() {
      const existingToken = getToken();


      if (!existingToken) {
        setLoading(false);
        return;
      }


      try {
        const { data } = await api.get("/auth/me");
        setUser(data);
        setToken(existingToken);
      } catch {
        clearAuthSession();
        setToken(null);
        setUser(null);
      } finally {
        setLoading(false);
      }
    }


    bootstrap();
  }, []);


  async function login(email, password) {
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);


    const { data } = await api.post("/auth/login", formData, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });


    const accessToken = data.access_token;
    setAuthSession(accessToken);


    const me = await api.get("/auth/me");
    setAuthSession(accessToken, me.data);


    setToken(accessToken);
    setUser(me.data);


    return me.data;
  }


  async function register(email, password) {
    const reg = await api.post("/auth/register", { email, password });


    if (reg.data.verification_required && reg.data.verification_token) {
      await api.get(`/auth/verify-email?token=${reg.data.verification_token}`);
    }


    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);


    const loginResp = await api.post("/auth/login", formData, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });


    const accessToken = loginResp.data.access_token;
    setAuthSession(accessToken);


    const me = await api.get("/auth/me");
    setAuthSession(accessToken, me.data);


    setToken(accessToken);
    setUser(me.data);


    return me.data;
  }


  function logout() {
    clearAuthSession();
    setToken(null);
    setUser(null);
  }


  const value = useMemo(
    () => ({
      token,
      user,
      loading,
      login,
      register,
      logout,
      isAuthenticated: !!token,
    }),
    [token, user, loading]
  );


  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}


export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}