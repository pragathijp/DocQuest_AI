// pages/index.tsx
import type { NextPage } from "next";
import Head from "next/head";
import { Chat } from "../components/Chat";

const Home: NextPage = () => {
  return (
    <>
      <Head>
        <title>DocMind — PDF Chat</title>
        <meta name="description" content="Chat with your PDF documents using AI" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Chat />
    </>
  );
};

export default Home;
