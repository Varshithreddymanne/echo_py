import { Box, Text, Heading, Button, HStack, VStack, Input } from "@chakra-ui/react";
import API from "../api";
import { useState, useEffect } from "react";

export default function PostCard({ post, refresh }) {
  const [comments, setComments] = useState([]);
  const [commentText, setCommentText] = useState("");

  const loadComments = async () => {
    try {
      const res = await API.get(`/posts/${post._id}/comments`);
      setComments(res.data);
    } catch (e) {
      setComments([]);
    }
  };

  useEffect(() => {
    loadComments();
  }, [post._id]);

  const like = async () => {
    await API.post(`/posts/${post._id}/like`);
    refresh();
  };

  const addComment = async () => {
    if (!commentText) return;
    await API.post(`/posts/${post._id}/comment`, {
      post_id: post._id,
      username: localStorage.getItem("username") || "anonymous",
      text: commentText,
    });
    setCommentText("");
    loadComments(); 
    refresh();
  };

  return (
    <Box borderWidth="1px" borderRadius="md" p={4} my={3}>
      <Heading size="sm">{post.title}</Heading>
      <Text>{post.content}</Text>
      <Text fontSize="sm" color="gray.500">By {post.username || "unknown"}</Text>
      <HStack mt={3}>
        <Button size="sm" onClick={like}>Like ({post.likes || 0})</Button>
      </HStack>
      <VStack mt={3} align="stretch">
        <Input value={commentText} placeholder="Add a comment" onChange={(e)=>setCommentText(e.target.value)} />
        <Button size="sm" onClick={addComment}>Comment</Button>
      </VStack>
      <VStack mt={3} align="stretch">
        {comments.length === 0 ? (
          <Text fontSize="sm" color="gray.400">No comments yet.</Text>
        ) : (
          comments.map(c => (
            <Box key={c._id} borderBottomWidth="1px" pb={2}>
              <Text fontWeight="bold" fontSize="sm">{c.username}</Text>
              <Text fontSize="sm">{c.text}</Text>
              <Text fontSize="xs" color="gray.500">{new Date(c.created_at).toLocaleString()}</Text>
            </Box>
          ))
        )}
      </VStack>
    </Box>
  );
}
