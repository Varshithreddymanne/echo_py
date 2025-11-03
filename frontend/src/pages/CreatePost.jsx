import { useState } from "react";
import { VStack, Input, Textarea, Button, Heading, useToast } from "@chakra-ui/react";
import API from "../api";
import { useNavigate } from "react-router-dom";

export default function CreatePost() {
  const [form, setForm] = useState({ title: "", content: "", username: "" });
  const toast = useToast();
  const nav = useNavigate();

  const handleCreate = async () => {
    try {
      await API.post("/posts", form);
      toast({ title: "Created post", status: "success" });
      nav("/");
    } catch (err) {
      toast({ title: "Error creating post", status: "error" });
    }
  };

  return (
    <VStack spacing={4} p={6}>
      <Heading size="md">Create Post</Heading>
      <Input placeholder="Username" onChange={(e) => setForm({ ...form, username: e.target.value })} />
      <Input placeholder="Title" onChange={(e) => setForm({ ...form, title: e.target.value })} />
      <Textarea placeholder="Content" onChange={(e) => setForm({ ...form, content: e.target.value })} />
      <Button onClick={handleCreate}>Create</Button>
    </VStack>
  );
}
