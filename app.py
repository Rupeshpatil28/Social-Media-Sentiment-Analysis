import os
import pickle
import glob
import requests

import streamlit as st
import tensorflow as tf


st.set_page_config(
    page_title="Social Media Sentiment Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)


st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --ink: #f8fafc;
    --muted: #aab7d2;
    --muted-bright: #d7def0;
    --panel: rgba(20, 27, 61, 0.72);
    --panel-light: rgba(32, 39, 81, 0.64);
    --line: rgba(153, 137, 255, 0.24);
    --purple: #a78bfa;
    --blue: #60a5fa;
}

* { font-family: 'Inter', sans-serif; }
.stApp {
    color: var(--ink);
    background:
        radial-gradient(circle at 8% 4%, rgba(93, 78, 210, .38), transparent 27rem),
        radial-gradient(circle at 92% 16%, rgba(40, 104, 218, .25), transparent 25rem),
        radial-gradient(circle at 50% 100%, rgba(119, 55, 195, .16), transparent 32rem),
        #080b1d;
}
.stApp > header {
    background: #080b1d !important; height: 2.75rem; z-index: 1000;
}
.block-container { max-width: 1240px; padding: 5.5rem 2.5rem 3.5rem; }
#MainMenu, footer { visibility: hidden; }
.stApp::before {
    content: ''; position: fixed; inset: 0; pointer-events: none; opacity: .22;
    background-image: linear-gradient(rgba(167,139,250,.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(96,165,250,.06) 1px, transparent 1px);
    background-size: 70px 70px; mask-image: linear-gradient(to bottom, #000, transparent 78%);
    animation: gridDrift 22s linear infinite; z-index: 0;
}
.ambient-orb {
    position: fixed; width: 19rem; height: 19rem; border-radius: 50%;
    filter: blur(55px); opacity: .16; pointer-events: none; z-index: 0;
}
.orb-left { left: -8rem; top: 38%; background: #7c3aed; animation: driftLeft 11s ease-in-out infinite; }
.orb-right { right: -8rem; top: 62%; background: #2563eb; animation: driftRight 13s ease-in-out infinite; }
.block-container { position: relative; z-index: 1; }

.dashboard-nav {
    position: sticky; top: 3rem; z-index: 999; width: 100%; box-sizing: border-box;
    display: flex; justify-content: space-between; align-items: center; margin-bottom: 4.5rem;
    padding: .9rem 1rem; color: #aeb9d5; font-size: .76rem; letter-spacing: .12em;
    text-transform: uppercase; background: rgba(8, 11, 29, .92);
    border: 1px solid rgba(167,139,250,.2); border-radius: 16px;
    box-shadow: 0 12px 30px rgba(0,0,0,.2); backdrop-filter: blur(16px);
}
.brand-mark { color: #fff; font-weight: 800; letter-spacing: -.02em; font-size: .95rem; text-transform: none; }
.brand-mark span { color: #a78bfa; }
.nav-status { color: #86efac; font-weight: 700; }
.hero { text-align: center; animation: fadeIn .9s ease both; margin-bottom: 3.8rem; }
.hero::after {
    content: ''; display: block; width: 9rem; height: 2px; margin: 2rem auto 0;
    background: linear-gradient(90deg, transparent, #a78bfa, #60a5fa, transparent);
    box-shadow: 0 0 18px #8b5cf6; animation: linePulse 2.5s ease-in-out infinite;
}
.hero-kicker {
    display: inline-block; color: #c4b5fd; text-transform: uppercase;
    letter-spacing: .18em; font-size: .72rem; font-weight: 700; margin-bottom: .9rem;
}
.hero-title {
    color: var(--ink) !important; font-size: clamp(2.35rem, 6vw, 4.6rem);
    line-height: 1.08; letter-spacing: -.065em; font-weight: 800; margin: 0;
}
.gradient-text {
    background: linear-gradient(100deg, #93c5fd 0%, #a78bfa 45%, #f0abfc 100%);
    -webkit-background-clip: text; background-clip: text; color: transparent;
}
.hero-subtitle { color: var(--muted); font-size: 1.08rem; margin: 1rem auto 1.35rem; }
.hero-badge, .status-pill {
    display: inline-flex; align-items: center; gap: .5rem; color: #e9ddff;
    background: linear-gradient(110deg, rgba(124, 92, 255, .23), rgba(54, 126, 255, .15));
    border: 1px solid rgba(167, 139, 250, .48); border-radius: 999px;
    padding: .58rem 1.15rem; font-size: .78rem; font-weight: 700;
    box-shadow: 0 0 24px rgba(124, 92, 255, .16); animation: pulseGlow 2.8s ease-in-out infinite;
}
.hero-badge { animation: pulseGlow 2.8s ease-in-out infinite, badgeFloat 4s ease-in-out infinite; }
.section-heading { color: var(--ink) !important; font-size: 1.55rem; font-weight: 800; margin: 2.2rem 0 .25rem; }
.section-copy { color: var(--muted) !important; margin: 0 0 1.1rem; font-size: .92rem; }
div[data-testid="stMarkdownContainer"] p, div[data-testid="stCaptionContainer"] { color: var(--muted); }

.input-card, .result-shell, .glass-card, .about-card {
    background: linear-gradient(145deg, rgba(31, 39, 86, .82), rgba(15, 20, 48, .78));
    border: 1px solid var(--line); border-radius: 24px; padding: 1.5rem;
    box-shadow: 0 18px 60px rgba(0, 0, 0, .25), inset 0 1px 0 rgba(255,255,255,.05);
    position: relative; overflow: hidden; animation: slideUp .7s ease both;
}
.input-card { padding: 1.85rem; }
.input-card:hover { border-color: rgba(167,139,250,.62); box-shadow: 0 22px 70px rgba(49, 35, 135, .3), inset 0 1px 0 rgba(255,255,255,.08); transition: .35s ease; }
.card-eyebrow { color: #9b8cff; text-transform: uppercase; letter-spacing: .15em; font-size: .68rem; font-weight: 800; }
.input-heading { color: #fff; font-size: 1.35rem; font-weight: 800; margin: .35rem 0 .2rem; }
.input-description { color: var(--muted); font-size: .86rem; margin: 0 0 1.2rem; }
.input-card::before, .glass-card::before, .about-card::before {
    content: ''; position: absolute; inset: 0; pointer-events: none;
    background: linear-gradient(120deg, rgba(167,139,250,.10), transparent 35%, rgba(96,165,250,.08));
}
.input-card h3, .glass-card h3, .about-card h3 { color: var(--ink) !important; margin: 0 0 .35rem; }
.input-card p, .glass-card p, .about-card p { color: var(--muted-bright) !important; line-height: 1.65; }
textarea {
    color: #fff !important; background: rgba(7, 11, 31, .72) !important;
    border: 1px solid rgba(148, 163, 184, .25) !important; border-radius: 16px !important;
    font-size: 1rem !important; padding: 1rem !important;
}
textarea::placeholder { color: #8794b2 !important; opacity: 1 !important; }
textarea:focus { border-color: var(--purple) !important; box-shadow: 0 0 0 1px var(--purple), 0 0 24px rgba(167,139,250,.2) !important; }
.stButton > button {
    width: 100%; min-height: 3.7rem; color: #fff !important;
    border: 1px solid rgba(196,181,253,.72); border-radius: 16px;
    background: linear-gradient(105deg, #5b3fe8 0%, #7c3aed 48%, #2563eb 100%);
    font-size: 1.05rem; letter-spacing: .01em; font-weight: 800; position: relative; overflow: hidden;
    box-shadow: 0 0 0 1px rgba(96,165,250,.14), 0 12px 32px rgba(91,63,232,.34);
    animation: analyzeGlow 2.8s ease-in-out infinite;
    transition: transform .25s ease, box-shadow .25s ease, filter .25s ease;
}
.stButton > button::after {
    content: ''; position: absolute; top: -80%; left: -35%; width: 22%; height: 260%;
    background: rgba(255,255,255,.24); transform: rotate(25deg); transition: left .7s ease;
}
.stButton > button:hover::after { left: 125%; }
.stButton > button:active { transform: translateY(1px) scale(.985); }
.stButton > button p { position: relative; z-index: 1;
}
.stButton > button:hover {
    color: #fff !important; transform: translateY(-4px) scale(1.01); filter: brightness(1.15);
    box-shadow: 0 0 0 2px rgba(196,181,253,.22), 0 16px 42px rgba(99,102,241,.58);
    animation: none;
}
.example-row .stButton > button { background: rgba(54, 64, 116, .55); border-color: rgba(148,163,184,.18); font-size: .82rem; }
.meta-line { color: #91a0c0; text-align: right; font-size: .75rem; margin: .45rem .1rem 0; }

.result-shell { margin-top: 2rem; border-color: rgba(96,165,250,.28); animation: resultReveal .9s cubic-bezier(.2,.8,.2,1) both; }
.result-shell::after {
    content: ''; position: absolute; width: 18rem; height: 18rem; right: -7rem; top: -9rem;
    border-radius: 50%; background: rgba(96,165,250,.12); filter: blur(12px); pointer-events: none;
}
.result-label { color: #94a3ff; font-size: .7rem; text-transform: uppercase; letter-spacing: .16em; font-weight: 800; }
.result-sentiment { color: var(--ink); font-size: 2rem; font-weight: 800; margin: .35rem 0 0; }
.result-sentiment.positive { color: #86efac; } .result-sentiment.negative { color: #fda4af; }
.metric-card {
    background: rgba(8, 13, 36, .64); border: 1px solid rgba(148,163,184,.16);
    border-radius: 16px; padding: 1rem; height: 100%; box-sizing: border-box;
}
.metric-card:hover { border-color: rgba(167,139,250,.5); transform: translateY(-2px); transition: .25s ease; }
.metric-name { color: #91a0c0; font-size: .75rem; margin-bottom: .4rem; }
.metric-value { color: #fff; font-size: 1.25rem; font-weight: 800; }
.confidence-track { height: .7rem; background: #252b50; border-radius: 99px; overflow: hidden; margin-top: .65rem; }
.confidence-fill { height: 100%; border-radius: inherit; background: linear-gradient(90deg, #6366f1, #a78bfa, #60a5fa); animation: growBar 1.2s ease-out both; transform-origin: left; }
.confidence-copy { color: var(--muted); font-size: .78rem; margin-top: .55rem; }

.glass-card { min-height: 142px; transition: transform .3s ease, border-color .3s ease, box-shadow .3s ease; }
.step-1 { animation-delay: .08s; } .step-2 { animation-delay: .2s; } .step-3 { animation-delay: .32s; }
.glass-card:hover { transform: translateY(-8px); border-color: rgba(167,139,250,.72); box-shadow: 0 18px 40px rgba(76, 55, 170, .25), 0 0 25px rgba(96,165,250,.1); }
.step-number { color: #a78bfa; font-size: .72rem; letter-spacing: .12em; font-weight: 800; }
.about-card { margin-top: 1.6rem; }
.about-card strong { color: #fff; }
.footer-wrap { text-align: center; margin: 3.5rem 0 1rem; padding-top: 2rem; border-top: 1px solid rgba(148,163,184,.14); }
.footer-name {
    font-size: 1.1rem; font-weight: 800;
    background: linear-gradient(90deg, #93c5fd, #c4b5fd, #f0abfc, #93c5fd);
    background-size: 220% auto; -webkit-background-clip: text; background-clip: text; color: transparent;
    animation: gradientShift 4s linear infinite;
}
.footer-copy { color: #8996b5; font-size: .78rem; line-height: 1.7; margin-top: .45rem; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(-12px); } to { opacity: 1; transform: translateY(0); } }
@keyframes slideUp { from { opacity: 0; transform: translateY(18px); } to { opacity: 1; transform: translateY(0); } }
@keyframes pulseGlow { 0%,100% { box-shadow: 0 0 20px rgba(124,92,255,.12); } 50% { box-shadow: 0 0 30px rgba(124,92,255,.32); } }
@keyframes growBar { from { transform: scaleX(0); } to { transform: scaleX(1); } }
@keyframes gradientShift { to { background-position: 220% center; } }
@keyframes gridDrift { to { background-position: 70px 70px; } }
@keyframes driftLeft { 0%,100% { transform: translate(0,0) scale(1); } 50% { transform: translate(70px,-45px) scale(1.18); } }
@keyframes driftRight { 0%,100% { transform: translate(0,0) scale(1); } 50% { transform: translate(-60px,35px) scale(.82); } }
@keyframes badgeFloat { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-4px); } }
@keyframes linePulse { 0%,100% { opacity: .45; width: 7rem; } 50% { opacity: 1; width: 13rem; } }
@keyframes resultReveal { from { opacity: 0; transform: translateY(28px) scale(.98); } to { opacity: 1; transform: translateY(0) scale(1); } }
@keyframes analyzeGlow {
    0%, 100% { box-shadow: 0 0 0 1px rgba(96,165,250,.14), 0 12px 32px rgba(91,63,232,.34); }
    50% { box-shadow: 0 0 0 3px rgba(167,139,250,.16), 0 16px 42px rgba(91,63,232,.52); }
}
@media (max-width: 720px) { .block-container { padding: 2rem 1rem; } .hero-title { font-size: 2.5rem; } }
/* Premium single-flow refinements */
.dashboard-nav { max-width: 1200px; margin: 0 auto 4.5rem; }
.hero { max-width: 1200px; margin: 0 auto 5.5rem; }
.hero-title { font-size: clamp(2.45rem, 5.5vw, 4.35rem); }
.section-heading { margin-top: 0; font-size: 1.75rem; letter-spacing: -.035em; }
.analysis-flow, .result-flow, .process-flow, .insight-flow, .technology-flow, .about-flow, .footer-wrap {
    width: 100%; max-width: 1200px; margin-left: auto; margin-right: auto;
}
.analysis-flow { margin-bottom: 6.5rem; }
.input-card {
    background: rgba(18, 24, 57, .66); border-color: rgba(167, 139, 250, .28);
    border-radius: 28px; padding: 2.4rem 2.6rem; box-shadow: 0 24px 70px rgba(0,0,0,.24);
}
.input-card::before { background: linear-gradient(120deg, rgba(167,139,250,.09), transparent 42%); }
.input-heading { font-size: 1.55rem; }
.input-description { font-size: .95rem; margin-bottom: 1.55rem; }
.input-card .stTextArea { margin-top: .2rem; }
.analysis-flow > div[data-testid="stButton"] { max-width: 420px; margin: 1.35rem auto 0; }
.analysis-flow > div[data-testid="stButton"]::before {
    content: 'READY TO ANALYZE'; display: block; color: #98a7c8; font-size: .64rem;
    font-weight: 800; letter-spacing: .16em; text-align: center; margin-bottom: .55rem;
}
.result-flow { margin-bottom: 6.5rem; }
.result-shell { margin-top: 0; border-radius: 28px; padding: 2.5rem 2.6rem; }
.result-sentiment { font-size: clamp(2rem, 4vw, 3rem); letter-spacing: -.045em; margin-bottom: .45rem; }
.result-shell > .section-copy { margin-bottom: 1.8rem; }
.metric-card {
    background: transparent; border: 0; border-left: 1px solid rgba(148,163,184,.2);
    border-radius: 0; padding: .25rem 1.25rem; box-shadow: none;
}
.metric-card:hover { transform: none; border-color: rgba(148,163,184,.2); }
.result-metrics { display: grid; grid-template-columns: repeat(3, 1fr); margin-top: .4rem; }
.metric-name { text-transform: uppercase; letter-spacing: .09em; font-size: .66rem; }
.metric-value { font-size: 1.45rem; }
.confidence-track { height: .8rem; margin-top: .9rem; background: rgba(148,163,184,.16); }
.confidence-copy { font-size: .82rem; }
.process-flow { margin-bottom: 5.5rem; }
.process-flow .section-copy { margin-bottom: 2.1rem; }
.glass-card {
    min-height: 0; padding: .2rem 1.7rem .2rem 0; background: transparent;
    border: 0; border-right: 1px solid rgba(148,163,184,.18); border-radius: 0;
    box-shadow: none; animation: slideUp .7s ease both;
}
.glass-card:hover { transform: translateY(-3px); border-color: rgba(148,163,184,.3); box-shadow: none; }
.glass-card::before { display: none; }
.how-col-last .glass-card { border-right: 0; padding-right: 0; }
.step-number { font-size: .78rem; color: #c4b5fd; }
.glass-card p { margin: .7rem 0 0; font-size: .9rem; color: var(--muted) !important; }
.about-flow { margin-bottom: 5.5rem; }
div[data-testid="stExpander"] {
    background: transparent; border: 0; border-top: 1px solid rgba(148,163,184,.18);
    border-bottom: 1px solid rgba(148,163,184,.18); border-radius: 0; padding: .65rem 0;
}
div[data-testid="stExpander"] summary, div[data-testid="stExpander"] summary span {
    color: #fff !important; font-size: 1rem; font-weight: 700;
}
div[data-testid="stExpander"] [data-testid="stMarkdownContainer"] p { color: var(--muted-bright) !important; }
.footer-wrap { margin-top: 3.5rem; padding-top: 2.2rem; }
.footer-copy { color: #8f9bb7; }
@media (max-width: 720px) {
    .stApp > header { height: 2.5rem; }
    .block-container { padding: 4.75rem 1rem 2rem; }
    .dashboard-nav { margin-bottom: 3rem; }
    .dashboard-nav { top: 2.75rem; padding: .8rem .75rem; }
    .hero { margin-bottom: 4rem; }
    .input-card, .result-shell { padding: 1.55rem; }
    .metric-card { border-left: 0; border-top: 1px solid rgba(148,163,184,.16); padding: .85rem 0; }
    .result-metrics { grid-template-columns: 1fr; }
    .glass-card { border-right: 0; border-bottom: 1px solid rgba(148,163,184,.18); padding: 1rem 0; }
    .timeline { grid-template-columns: 1fr; gap: 0; }
    .timeline-step { min-height: 0; padding: 1.25rem 0; text-align: left; border-right: 0; border-bottom: 1px solid rgba(148,163,184,.16); }
    .timeline-step:last-child { border-bottom: 0; }
    .timeline-step::after { top: auto; bottom: -.45rem; right: auto; left: 2rem; width: 1px; height: .9rem; }
    .timeline-step:last-child::after { display: none; }
    .timeline-step p { margin-left: 0; }
}
.nav-links { display: flex; align-items: center; gap: 1.35rem; margin-left: auto; margin-right: 1.5rem; }
.nav-links a { color: #aeb9d5; text-decoration: none; font-size: .72rem; letter-spacing: .04em; text-transform: none; transition: color .2s ease; }
.nav-links a:hover { color: #fff; }
.analysis-flow, .result-flow, .process-flow, .insight-flow, .technology-flow, .about-flow, .footer-wrap { scroll-margin-top: 7rem; }
.insight-flow, .technology-flow { margin-bottom: 5.5rem; }
.pipeline { display: flex; align-items: center; justify-content: space-between; gap: .7rem; margin-top: 2.2rem; }
.pipeline-node { display: flex; flex-direction: column; align-items: center; justify-content: center; min-width: 8rem; min-height: 5.2rem; padding: .65rem; color: #f8fafc; background: rgba(23, 31, 73, .78); border: 1px solid rgba(167,139,250,.48); border-radius: 18px; box-shadow: 0 0 22px rgba(124,92,255,.16); }
.pipeline-node span { color: #d8ccff; font-size: .72rem; font-weight: 800; letter-spacing: .08em; }
.pipeline-node small { color: #91a0c0; margin-top: .35rem; font-size: .68rem; }
.pipeline-connector { flex: 1; height: 1px; min-width: 1rem; background: linear-gradient(90deg, #8b5cf6, #60a5fa); box-shadow: 0 0 10px rgba(139,92,246,.7); }
.timeline { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0; margin-top: 2.2rem; }
.timeline-step { position: relative; min-height: 10rem; padding: 0 1.4rem; text-align: center; border-right: 1px solid rgba(148,163,184,.16); transition: transform .25s ease; }
.timeline-step:last-child { border-right: 0; }
.timeline-step::after { content: ''; position: absolute; top: 2.4rem; right: -.45rem; width: .9rem; height: 1px; background: #8b5cf6; box-shadow: 0 0 10px rgba(96,165,250,.7); }
.timeline-step:last-child::after { display: none; }
.timeline-step:hover { transform: translateY(-4px); }
.timeline-step:hover .timeline-icon { transform: scale(1.12); }
.timeline-step:hover .timeline-title { color: #d8ccff; }
.timeline-number { color: #c4b5fd; font-size: 1.25rem; font-weight: 800; letter-spacing: .08em; }
.timeline-icon { margin: .7rem 0; font-size: 1.25rem; transition: transform .25s ease; }
.timeline-title { color: #fff; font-size: .8rem; font-weight: 800; letter-spacing: .12em; transition: color .25s ease; }
.timeline-step p { margin: .6rem auto 0; max-width: 15rem; color: var(--muted) !important; font-size: .86rem; line-height: 1.55; }
.tech-pills { display: flex; flex-wrap: wrap; gap: .65rem; margin-top: 1.2rem; }
.tech-pills span { color: #d9d5ff; background: rgba(36, 43, 91, .68); border: 1px solid rgba(167,139,250,.28); border-radius: 999px; padding: .58rem .85rem; font-size: .78rem; }
.about-card { margin-top: 1.2rem; padding: 1.7rem 2rem; }
.about-card p { margin: 0 0 .75rem; }
.about-card p:last-child { margin-bottom: 0; }
.footer-wrap + div[data-testid="stExpander"] { width: 100%; max-width: 1200px; margin: 1rem auto 0; }
.footer-wrap + div[data-testid="stExpander"] summary { padding: .85rem 1rem; }
.team-list { display: grid; gap: .7rem; padding: .8rem .25rem .35rem; }
.team-member { display: flex; align-items: center; gap: .8rem; color: var(--muted-bright); font-size: .9rem; }
.team-avatar { display: inline-flex; align-items: center; justify-content: center; width: 2rem; height: 2rem; border-radius: 50%; color: #fff; font-size: .68rem; font-weight: 800; background: linear-gradient(135deg, #7c3aed, #2563eb); box-shadow: 0 0 16px rgba(124,92,255,.35); }
@media (max-width: 860px) {
    .dashboard-nav { flex-wrap: wrap; gap: .7rem; }
    .nav-links { order: 3; width: 100%; justify-content: center; margin: .25rem 0 0; gap: .8rem; }
    .nav-status { margin-left: auto; }
    .pipeline { flex-wrap: wrap; justify-content: center; }
    .pipeline-connector { flex: 0 0 2rem; }
}
@media (max-width: 560px) {
    .pipeline-connector { display: none; }
    .pipeline-node { flex: 1 1 7rem; min-width: 6.5rem; }
    .nav-links { gap: .45rem; justify-content: space-between; }
    .nav-links a { font-size: .64rem; }
    .about-card { padding: 1.3rem; }
}
/* Final layout and team presentation */
.dashboard-nav, .hero, .analysis-flow, .result-flow, .insight-flow,
.process-flow, .technology-flow, .about-flow, .footer-wrap,
.footer-wrap + div[data-testid="stExpander"], .about-flow + div[data-testid="stExpander"] {
    box-sizing: border-box;
    width: 100%;
    max-width: 1200px;
    margin-left: auto;
    margin-right: auto;
    padding-left: 32px;
    padding-right: 32px;
}
.process-flow { margin-top: 0; margin-bottom: 5.5rem; }
.process-flow .section-heading { margin-bottom: 0; }
.process-flow .section-copy { margin: 16px 0 42px; }
.timeline { margin-top: 0; }
.timeline-step { min-width: 0; }
div[data-testid="stExpander"] {
    box-sizing: border-box;
    background: rgba(12, 17, 43, .82) !important;
    border: 1px solid rgba(167, 139, 250, .28) !important;
    border-radius: 16px !important;
    padding: 0 !important;
    overflow: hidden;
}
div[data-testid="stExpander"] details,
div[data-testid="stExpander"] details[open],
div[data-testid="stExpander"] summary,
div[data-testid="stExpander"] summary:hover,
div[data-testid="stExpander"] summary:focus,
div[data-testid="stExpander"] summary:focus-visible {
    color: #f8fafc !important;
    background: rgba(12, 17, 43, .82) !important;
}
div[data-testid="stExpander"] summary {
    min-height: 3.1rem;
    padding: .85rem 1rem !important;
    outline: none !important;
}
div[data-testid="stExpander"] summary span,
div[data-testid="stExpander"] summary p,
div[data-testid="stExpander"] summary svg {
    color: #f8fafc !important;
    fill: #f8fafc !important;
}
div[data-testid="stExpander"] summary:hover span,
div[data-testid="stExpander"] summary:hover p,
div[data-testid="stExpander"] summary:hover svg {
    color: #d8ccff !important;
    fill: #d8ccff !important;
}
div[data-testid="stExpander"] > details > div {
    background: rgba(12, 17, 43, .72) !important;
    border-top: 1px solid rgba(148, 163, 184, .14);
    padding: .7rem 1rem 1rem !important;
}
.team-member { padding: .3rem .45rem; border-radius: 10px; transition: background .2s ease, transform .2s ease; }
.team-member:hover { background: rgba(124, 92, 255, .12); transform: translateX(4px); }
.footer-wrap { margin-top: 1.8rem; }
.footer-wrap + div[data-testid="stExpander"], .about-flow + div[data-testid="stExpander"] { margin-top: 0; margin-bottom: 1.8rem; }
@media (max-width: 720px) {
    .dashboard-nav, .hero, .analysis-flow, .result-flow, .insight-flow,
    .process-flow, .technology-flow, .about-flow, .footer-wrap,
    .footer-wrap + div[data-testid="stExpander"], .about-flow + div[data-testid="stExpander"] {
        padding-left: 32px;
        padding-right: 32px;
    }
}
</style>
""",
    unsafe_allow_html=True,
)



@st.cache_resource
def load_model():
    model_url = "https://huggingface.co/RupeshP28/social-media-sentiment-model/resolve/main/lstm_model.h5"
    model_path = os.path.join("models", "lstm_model.h5")

    os.makedirs("models", exist_ok=True)

    if not os.path.exists(model_path):
        response = requests.get(model_url, stream=True)
        response.raise_for_status()

        with open(model_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

    return tf.keras.models.load_model(model_path)



@st.cache_resource
def load_tokenizer():
    possible_paths = [
        os.path.join("models", "tokenizer.pkl"),
        os.path.join("models", "tokenizer.pickle"),
    ]
    possible_paths.extend(glob.glob(os.path.join("models", "*tokenizer*.pkl")))
    possible_paths.extend(glob.glob(os.path.join("models", "*tokenizer*.pickle")))
    tokenizer_path = None
    for path in possible_paths:
        if os.path.exists(path):
            tokenizer_path = path
            break
    if tokenizer_path is None:
        st.error(
            "Tokenizer file was not found inside the `models` folder.\n\n"
            "Expected something like `tokenizer.pkl`."
        )
        st.stop()
    with open(tokenizer_path, "rb") as file:
        tokenizer = pickle.load(file)
    return tokenizer


model = load_model()
tokenizer = load_tokenizer()

if "tweet_input" not in st.session_state:
    st.session_state.tweet_input = ""


st.markdown(
    """
<div class="ambient-orb orb-left"></div>
<div class="ambient-orb orb-right"></div>
<div class="dashboard-nav">
    <div class="brand-mark">🧠 Sentiment<span>AI</span></div>
    <div class="nav-links">
        <a href="#home">Home</a>
        <a href="#analyze">Analyze</a>
        <a href="#how-it-works">How It Works</a>
        <a href="#technology">Technology</a>
        <a href="#about">About</a>
    </div>
    <div class="nav-status">● SYSTEM READY</div>
</div>
<div id="home" class="hero">
    <div class="hero-kicker">Social intelligence, powered by deep learning</div>
    <h1 class="hero-title">🧠 <span class="gradient-text">Social Media Sentiment Intelligence</span></h1>
    <div class="hero-subtitle">AI-powered sentiment analysis using NLP, GloVe embeddings and LSTM deep learning.</div>
    <div class="hero-badge">⚡ AI <span>•</span> NLP <span>•</span> LSTM</div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('<div id="analyze" class="analysis-flow">', unsafe_allow_html=True)
st.markdown(
    """
<div class="input-card">
    <div class="card-eyebrow">Analysis workspace</div>
    <div class="input-heading">Analyze Social Media Text</div>
    <div class="input-description">Enter a tweet or social media message and let the trained LSTM model analyze its sentiment.</div>
""",
    unsafe_allow_html=True,
)

tweet = st.text_area(
    "Tweet",
    value=st.session_state.tweet_input,
    height=155,
    placeholder="Example: I absolutely love this product! The experience was amazing.",
    label_visibility="collapsed",
    key="tweet_text_area",
)
if tweet:
    st.markdown(f'<div class="meta-line">{len(tweet)} characters</div>', unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

analyze = st.button("🔍 Analyze Sentiment", type="primary", key="analyze_button")
st.markdown("</div>", unsafe_allow_html=True)


if analyze:
    if not tweet.strip():
        st.warning("⚠️ Please enter a tweet or social media message first.")
    else:
        with st.spinner("🧠 Analyzing your text..."):
            sequence = tokenizer.texts_to_sequences([tweet])
            padded_sequence = tf.keras.preprocessing.sequence.pad_sequences(
                sequence,
                maxlen=30,
            )
            prediction = model.predict(padded_sequence, verbose=0)
            score = float(prediction[0][0])

        if score >= 0.5:
            sentiment = "Positive"
            emoji = "😊"
            confidence = score * 100
        else:
            sentiment = "Negative"
            emoji = "😞"
            confidence = (1 - score) * 100

        sentiment_class = sentiment.lower()
        st.markdown('<div class="result-flow">', unsafe_allow_html=True)
        st.markdown(
            f"""
<div class="result-shell">
    <div class="result-label">SENTIMENT RESULT</div>
    <div class="result-sentiment {sentiment_class}">{emoji} {sentiment} Sentiment</div>
    <p class="section-copy">The trained model has evaluated the emotional tone of your text.</p>
    <div class="card-eyebrow">Signal metrics</div>
""",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
    <div class="result-metrics">
        <div class="metric-card"><div class="metric-name">Prediction Score</div><div class="metric-value">{score:.4f}</div></div>
        <div class="metric-card"><div class="metric-name">Confidence</div><div class="metric-value">{confidence:.2f}%</div></div>
        <div class="metric-card"><div class="metric-name">Prediction</div><div class="metric-value">{emoji} {sentiment}</div></div>
    </div>
    <div class="metric-name" style="margin-top:1.8rem;">MODEL CONFIDENCE</div>
    <div class="confidence-track"><div class="confidence-fill" style="width:{min(max(confidence, 0), 100):.2f}%;"></div></div>
    <div class="confidence-copy">{confidence:.2f}% confidence in this classification</div>
</div>
""",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)


st.markdown(
    """
<div class="insight-flow">
    <div class="section-heading">🧠 What the AI Sees</div>
    <div class="section-copy">From words to sentiment — the model transforms social media language into a numerical representation before making a prediction.</div>
    <div class="pipeline">
        <div class="pipeline-node"><span>TEXT</span><small>raw language</small></div>
        <div class="pipeline-connector"></div>
        <div class="pipeline-node"><span>TOKENIZATION</span><small>sequence IDs</small></div>
        <div class="pipeline-connector"></div>
        <div class="pipeline-node"><span>GloVe</span><small>embeddings</small></div>
        <div class="pipeline-connector"></div>
        <div class="pipeline-node"><span>LSTM</span><small>context</small></div>
        <div class="pipeline-connector"></div>
        <div class="pipeline-node"><span>SCORE</span><small>sentiment</small></div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('<div id="how-it-works" class="process-flow"><div class="section-heading">How It Works</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-copy">From raw social text to an actionable sentiment signal.</div>',
    unsafe_allow_html=True,
)
steps = [
    ("01", "📝", "INPUT", "Social media text enters the analysis pipeline."),
    ("02", "🔤", "REPRESENTATION", "Words are converted into numerical representations using GloVe embeddings."),
    ("03", "🧠", "LSTM ANALYSIS", "The LSTM model learns contextual patterns in the text."),
    ("04", "📊", "PREDICTION", "The model generates a sentiment score and classification."),
]
timeline_html = '<div class="timeline">'
for number, icon, title, copy in steps:
    timeline_html += (
        f'<div class="timeline-step"><div class="timeline-number">{number}</div>'
        f'<div class="timeline-icon">{icon}</div><div class="timeline-title">{title}</div>'
        f'<p>{copy}</p></div>'
    )
timeline_html += "</div>"
st.markdown(timeline_html, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
<div id="technology" class="technology-flow">
    <div class="section-heading">⚙️ Technology Stack</div>
    <div class="tech-pills">
        <span>Python</span><span>TensorFlow / Keras</span><span>LSTM</span><span>NLP</span>
        <span>GloVe</span><span>NumPy</span><span>Pandas</span><span>Streamlit</span>
    </div>
</div>
<div id="about" class="about-flow">
    <div class="section-heading">ℹ️ About This Project</div>
    <div class="about-card">
        <p>This project uses Natural Language Processing, GloVe word embeddings and an LSTM deep learning model to classify social media text as positive or negative.</p>
        <p>The model converts text into sequences, represents words numerically and uses LSTM to capture contextual patterns before producing a sentiment score.</p>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

with st.expander("👥  Meet the Team"):
    st.markdown(
        """
<div class="team-list">
    <div class="team-member"><span class="team-avatar">RP</span><span>Rupesh Patil</span></div>
    <div class="team-member"><span class="team-avatar">VS</span><span>Vishal Sahane</span></div>
    <div class="team-member"><span class="team-avatar">ON</span><span>Om Nikumbh</span></div>
    <div class="team-member"><span class="team-avatar">KP</span><span>Kaustubh Patil</span></div>
</div>
""",
        unsafe_allow_html=True,
    )

st.markdown(
    """
<div class="footer-wrap">
    <div class="footer-name">Social Media Sentiment Intelligence</div>
    <div class="footer-copy">Built as a Team Project • 2026<br>Developed collaboratively by the team.</div>
</div>
""",
    unsafe_allow_html=True,
)

import os
import pickle
import glob

import streamlit as st
import tensorflow as tf


st.set_page_config(
    page_title="Social Media Sentiment Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)


st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --ink: #f8fafc;
    --muted: #aab7d2;
    --muted-bright: #d7def0;
    --panel: rgba(20, 27, 61, 0.72);
    --panel-light: rgba(32, 39, 81, 0.64);
    --line: rgba(153, 137, 255, 0.24);
    --purple: #a78bfa;
    --blue: #60a5fa;
}

* { font-family: 'Inter', sans-serif; }
.stApp {
    color: var(--ink);
    background:
        radial-gradient(circle at 8% 4%, rgba(93, 78, 210, .38), transparent 27rem),
        radial-gradient(circle at 92% 16%, rgba(40, 104, 218, .25), transparent 25rem),
        radial-gradient(circle at 50% 100%, rgba(119, 55, 195, .16), transparent 32rem),
        #080b1d;
}
.stApp > header {
    background: #080b1d !important; height: 2.75rem; z-index: 1000;
}
.block-container { max-width: 1240px; padding: 5.5rem 2.5rem 3.5rem; }
#MainMenu, footer { visibility: hidden; }
.stApp::before {
    content: ''; position: fixed; inset: 0; pointer-events: none; opacity: .22;
    background-image: linear-gradient(rgba(167,139,250,.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(96,165,250,.06) 1px, transparent 1px);
    background-size: 70px 70px; mask-image: linear-gradient(to bottom, #000, transparent 78%);
    animation: gridDrift 22s linear infinite; z-index: 0;
}
.ambient-orb {
    position: fixed; width: 19rem; height: 19rem; border-radius: 50%;
    filter: blur(55px); opacity: .16; pointer-events: none; z-index: 0;
}
.orb-left { left: -8rem; top: 38%; background: #7c3aed; animation: driftLeft 11s ease-in-out infinite; }
.orb-right { right: -8rem; top: 62%; background: #2563eb; animation: driftRight 13s ease-in-out infinite; }
.block-container { position: relative; z-index: 1; }

.dashboard-nav {
    position: sticky; top: 3rem; z-index: 999; width: 100%; box-sizing: border-box;
    display: flex; justify-content: space-between; align-items: center; margin-bottom: 4.5rem;
    padding: .9rem 1rem; color: #aeb9d5; font-size: .76rem; letter-spacing: .12em;
    text-transform: uppercase; background: rgba(8, 11, 29, .92);
    border: 1px solid rgba(167,139,250,.2); border-radius: 16px;
    box-shadow: 0 12px 30px rgba(0,0,0,.2); backdrop-filter: blur(16px);
}
.brand-mark { color: #fff; font-weight: 800; letter-spacing: -.02em; font-size: .95rem; text-transform: none; }
.brand-mark span { color: #a78bfa; }
.nav-status { color: #86efac; font-weight: 700; }
.hero { text-align: center; animation: fadeIn .9s ease both; margin-bottom: 3.8rem; }
.hero::after {
    content: ''; display: block; width: 9rem; height: 2px; margin: 2rem auto 0;
    background: linear-gradient(90deg, transparent, #a78bfa, #60a5fa, transparent);
    box-shadow: 0 0 18px #8b5cf6; animation: linePulse 2.5s ease-in-out infinite;
}
.hero-kicker {
    display: inline-block; color: #c4b5fd; text-transform: uppercase;
    letter-spacing: .18em; font-size: .72rem; font-weight: 700; margin-bottom: .9rem;
}
.hero-title {
    color: var(--ink) !important; font-size: clamp(2.35rem, 6vw, 4.6rem);
    line-height: 1.08; letter-spacing: -.065em; font-weight: 800; margin: 0;
}
.gradient-text {
    background: linear-gradient(100deg, #93c5fd 0%, #a78bfa 45%, #f0abfc 100%);
    -webkit-background-clip: text; background-clip: text; color: transparent;
}
.hero-subtitle { color: var(--muted); font-size: 1.08rem; margin: 1rem auto 1.35rem; }
.hero-badge, .status-pill {
    display: inline-flex; align-items: center; gap: .5rem; color: #e9ddff;
    background: linear-gradient(110deg, rgba(124, 92, 255, .23), rgba(54, 126, 255, .15));
    border: 1px solid rgba(167, 139, 250, .48); border-radius: 999px;
    padding: .58rem 1.15rem; font-size: .78rem; font-weight: 700;
    box-shadow: 0 0 24px rgba(124, 92, 255, .16); animation: pulseGlow 2.8s ease-in-out infinite;
}
.hero-badge { animation: pulseGlow 2.8s ease-in-out infinite, badgeFloat 4s ease-in-out infinite; }
.section-heading { color: var(--ink) !important; font-size: 1.55rem; font-weight: 800; margin: 2.2rem 0 .25rem; }
.section-copy { color: var(--muted) !important; margin: 0 0 1.1rem; font-size: .92rem; }
div[data-testid="stMarkdownContainer"] p, div[data-testid="stCaptionContainer"] { color: var(--muted); }

.input-card, .result-shell, .glass-card, .about-card {
    background: linear-gradient(145deg, rgba(31, 39, 86, .82), rgba(15, 20, 48, .78));
    border: 1px solid var(--line); border-radius: 24px; padding: 1.5rem;
    box-shadow: 0 18px 60px rgba(0, 0, 0, .25), inset 0 1px 0 rgba(255,255,255,.05);
    position: relative; overflow: hidden; animation: slideUp .7s ease both;
}
.input-card { padding: 1.85rem; }
.input-card:hover { border-color: rgba(167,139,250,.62); box-shadow: 0 22px 70px rgba(49, 35, 135, .3), inset 0 1px 0 rgba(255,255,255,.08); transition: .35s ease; }
.card-eyebrow { color: #9b8cff; text-transform: uppercase; letter-spacing: .15em; font-size: .68rem; font-weight: 800; }
.input-heading { color: #fff; font-size: 1.35rem; font-weight: 800; margin: .35rem 0 .2rem; }
.input-description { color: var(--muted); font-size: .86rem; margin: 0 0 1.2rem; }
.input-card::before, .glass-card::before, .about-card::before {
    content: ''; position: absolute; inset: 0; pointer-events: none;
    background: linear-gradient(120deg, rgba(167,139,250,.10), transparent 35%, rgba(96,165,250,.08));
}
.input-card h3, .glass-card h3, .about-card h3 { color: var(--ink) !important; margin: 0 0 .35rem; }
.input-card p, .glass-card p, .about-card p { color: var(--muted-bright) !important; line-height: 1.65; }
textarea {
    color: #fff !important; background: rgba(7, 11, 31, .72) !important;
    border: 1px solid rgba(148, 163, 184, .25) !important; border-radius: 16px !important;
    font-size: 1rem !important; padding: 1rem !important;
}
textarea::placeholder { color: #8794b2 !important; opacity: 1 !important; }
textarea:focus { border-color: var(--purple) !important; box-shadow: 0 0 0 1px var(--purple), 0 0 24px rgba(167,139,250,.2) !important; }
.stButton > button {
    width: 100%; min-height: 3.7rem; color: #fff !important;
    border: 1px solid rgba(196,181,253,.72); border-radius: 16px;
    background: linear-gradient(105deg, #5b3fe8 0%, #7c3aed 48%, #2563eb 100%);
    font-size: 1.05rem; letter-spacing: .01em; font-weight: 800; position: relative; overflow: hidden;
    box-shadow: 0 0 0 1px rgba(96,165,250,.14), 0 12px 32px rgba(91,63,232,.34);
    animation: analyzeGlow 2.8s ease-in-out infinite;
    transition: transform .25s ease, box-shadow .25s ease, filter .25s ease;
}
.stButton > button::after {
    content: ''; position: absolute; top: -80%; left: -35%; width: 22%; height: 260%;
    background: rgba(255,255,255,.24); transform: rotate(25deg); transition: left .7s ease;
}
.stButton > button:hover::after { left: 125%; }
.stButton > button:active { transform: translateY(1px) scale(.985); }
.stButton > button p { position: relative; z-index: 1;
}
.stButton > button:hover {
    color: #fff !important; transform: translateY(-4px) scale(1.01); filter: brightness(1.15);
    box-shadow: 0 0 0 2px rgba(196,181,253,.22), 0 16px 42px rgba(99,102,241,.58);
    animation: none;
}
.example-row .stButton > button { background: rgba(54, 64, 116, .55); border-color: rgba(148,163,184,.18); font-size: .82rem; }
.meta-line { color: #91a0c0; text-align: right; font-size: .75rem; margin: .45rem .1rem 0; }

.result-shell { margin-top: 2rem; border-color: rgba(96,165,250,.28); animation: resultReveal .9s cubic-bezier(.2,.8,.2,1) both; }
.result-shell::after {
    content: ''; position: absolute; width: 18rem; height: 18rem; right: -7rem; top: -9rem;
    border-radius: 50%; background: rgba(96,165,250,.12); filter: blur(12px); pointer-events: none;
}
.result-label { color: #94a3ff; font-size: .7rem; text-transform: uppercase; letter-spacing: .16em; font-weight: 800; }
.result-sentiment { color: var(--ink); font-size: 2rem; font-weight: 800; margin: .35rem 0 0; }
.result-sentiment.positive { color: #86efac; } .result-sentiment.negative { color: #fda4af; }
.metric-card {
    background: rgba(8, 13, 36, .64); border: 1px solid rgba(148,163,184,.16);
    border-radius: 16px; padding: 1rem; height: 100%; box-sizing: border-box;
}
.metric-card:hover { border-color: rgba(167,139,250,.5); transform: translateY(-2px); transition: .25s ease; }
.metric-name { color: #91a0c0; font-size: .75rem; margin-bottom: .4rem; }
.metric-value { color: #fff; font-size: 1.25rem; font-weight: 800; }
.confidence-track { height: .7rem; background: #252b50; border-radius: 99px; overflow: hidden; margin-top: .65rem; }
.confidence-fill { height: 100%; border-radius: inherit; background: linear-gradient(90deg, #6366f1, #a78bfa, #60a5fa); animation: growBar 1.2s ease-out both; transform-origin: left; }
.confidence-copy { color: var(--muted); font-size: .78rem; margin-top: .55rem; }

.glass-card { min-height: 142px; transition: transform .3s ease, border-color .3s ease, box-shadow .3s ease; }
.step-1 { animation-delay: .08s; } .step-2 { animation-delay: .2s; } .step-3 { animation-delay: .32s; }
.glass-card:hover { transform: translateY(-8px); border-color: rgba(167,139,250,.72); box-shadow: 0 18px 40px rgba(76, 55, 170, .25), 0 0 25px rgba(96,165,250,.1); }
.step-number { color: #a78bfa; font-size: .72rem; letter-spacing: .12em; font-weight: 800; }
.about-card { margin-top: 1.6rem; }
.about-card strong { color: #fff; }
.footer-wrap { text-align: center; margin: 3.5rem 0 1rem; padding-top: 2rem; border-top: 1px solid rgba(148,163,184,.14); }
.footer-name {
    font-size: 1.1rem; font-weight: 800;
    background: linear-gradient(90deg, #93c5fd, #c4b5fd, #f0abfc, #93c5fd);
    background-size: 220% auto; -webkit-background-clip: text; background-clip: text; color: transparent;
    animation: gradientShift 4s linear infinite;
}
.footer-copy { color: #8996b5; font-size: .78rem; line-height: 1.7; margin-top: .45rem; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(-12px); } to { opacity: 1; transform: translateY(0); } }
@keyframes slideUp { from { opacity: 0; transform: translateY(18px); } to { opacity: 1; transform: translateY(0); } }
@keyframes pulseGlow { 0%,100% { box-shadow: 0 0 20px rgba(124,92,255,.12); } 50% { box-shadow: 0 0 30px rgba(124,92,255,.32); } }
@keyframes growBar { from { transform: scaleX(0); } to { transform: scaleX(1); } }
@keyframes gradientShift { to { background-position: 220% center; } }
@keyframes gridDrift { to { background-position: 70px 70px; } }
@keyframes driftLeft { 0%,100% { transform: translate(0,0) scale(1); } 50% { transform: translate(70px,-45px) scale(1.18); } }
@keyframes driftRight { 0%,100% { transform: translate(0,0) scale(1); } 50% { transform: translate(-60px,35px) scale(.82); } }
@keyframes badgeFloat { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-4px); } }
@keyframes linePulse { 0%,100% { opacity: .45; width: 7rem; } 50% { opacity: 1; width: 13rem; } }
@keyframes resultReveal { from { opacity: 0; transform: translateY(28px) scale(.98); } to { opacity: 1; transform: translateY(0) scale(1); } }
@keyframes analyzeGlow {
    0%, 100% { box-shadow: 0 0 0 1px rgba(96,165,250,.14), 0 12px 32px rgba(91,63,232,.34); }
    50% { box-shadow: 0 0 0 3px rgba(167,139,250,.16), 0 16px 42px rgba(91,63,232,.52); }
}
@media (max-width: 720px) { .block-container { padding: 2rem 1rem; } .hero-title { font-size: 2.5rem; } }
/* Premium single-flow refinements */
.dashboard-nav { max-width: 1200px; margin: 0 auto 4.5rem; }
.hero { max-width: 1200px; margin: 0 auto 5.5rem; }
.hero-title { font-size: clamp(2.45rem, 5.5vw, 4.35rem); }
.section-heading { margin-top: 0; font-size: 1.75rem; letter-spacing: -.035em; }
.analysis-flow, .result-flow, .process-flow, .insight-flow, .technology-flow, .about-flow, .footer-wrap {
    width: 100%; max-width: 1200px; margin-left: auto; margin-right: auto;
}
.analysis-flow { margin-bottom: 6.5rem; }
.input-card {
    background: rgba(18, 24, 57, .66); border-color: rgba(167, 139, 250, .28);
    border-radius: 28px; padding: 2.4rem 2.6rem; box-shadow: 0 24px 70px rgba(0,0,0,.24);
}
.input-card::before { background: linear-gradient(120deg, rgba(167,139,250,.09), transparent 42%); }
.input-heading { font-size: 1.55rem; }
.input-description { font-size: .95rem; margin-bottom: 1.55rem; }
.input-card .stTextArea { margin-top: .2rem; }
.analysis-flow > div[data-testid="stButton"] { max-width: 420px; margin: 1.35rem auto 0; }
.analysis-flow > div[data-testid="stButton"]::before {
    content: 'READY TO ANALYZE'; display: block; color: #98a7c8; font-size: .64rem;
    font-weight: 800; letter-spacing: .16em; text-align: center; margin-bottom: .55rem;
}
.result-flow { margin-bottom: 6.5rem; }
.result-shell { margin-top: 0; border-radius: 28px; padding: 2.5rem 2.6rem; }
.result-sentiment { font-size: clamp(2rem, 4vw, 3rem); letter-spacing: -.045em; margin-bottom: .45rem; }
.result-shell > .section-copy { margin-bottom: 1.8rem; }
.metric-card {
    background: transparent; border: 0; border-left: 1px solid rgba(148,163,184,.2);
    border-radius: 0; padding: .25rem 1.25rem; box-shadow: none;
}
.metric-card:hover { transform: none; border-color: rgba(148,163,184,.2); }
.result-metrics { display: grid; grid-template-columns: repeat(3, 1fr); margin-top: .4rem; }
.metric-name { text-transform: uppercase; letter-spacing: .09em; font-size: .66rem; }
.metric-value { font-size: 1.45rem; }
.confidence-track { height: .8rem; margin-top: .9rem; background: rgba(148,163,184,.16); }
.confidence-copy { font-size: .82rem; }
.process-flow { margin-bottom: 5.5rem; }
.process-flow .section-copy { margin-bottom: 2.1rem; }
.glass-card {
    min-height: 0; padding: .2rem 1.7rem .2rem 0; background: transparent;
    border: 0; border-right: 1px solid rgba(148,163,184,.18); border-radius: 0;
    box-shadow: none; animation: slideUp .7s ease both;
}
.glass-card:hover { transform: translateY(-3px); border-color: rgba(148,163,184,.3); box-shadow: none; }
.glass-card::before { display: none; }
.how-col-last .glass-card { border-right: 0; padding-right: 0; }
.step-number { font-size: .78rem; color: #c4b5fd; }
.glass-card p { margin: .7rem 0 0; font-size: .9rem; color: var(--muted) !important; }
.about-flow { margin-bottom: 5.5rem; }
div[data-testid="stExpander"] {
    background: transparent; border: 0; border-top: 1px solid rgba(148,163,184,.18);
    border-bottom: 1px solid rgba(148,163,184,.18); border-radius: 0; padding: .65rem 0;
}
div[data-testid="stExpander"] summary, div[data-testid="stExpander"] summary span {
    color: #fff !important; font-size: 1rem; font-weight: 700;
}
div[data-testid="stExpander"] [data-testid="stMarkdownContainer"] p { color: var(--muted-bright) !important; }
.footer-wrap { margin-top: 3.5rem; padding-top: 2.2rem; }
.footer-copy { color: #8f9bb7; }
@media (max-width: 720px) {
    .stApp > header { height: 2.5rem; }
    .block-container { padding: 4.75rem 1rem 2rem; }
    .dashboard-nav { margin-bottom: 3rem; }
    .dashboard-nav { top: 2.75rem; padding: .8rem .75rem; }
    .hero { margin-bottom: 4rem; }
    .input-card, .result-shell { padding: 1.55rem; }
    .metric-card { border-left: 0; border-top: 1px solid rgba(148,163,184,.16); padding: .85rem 0; }
    .result-metrics { grid-template-columns: 1fr; }
    .glass-card { border-right: 0; border-bottom: 1px solid rgba(148,163,184,.18); padding: 1rem 0; }
    .timeline { grid-template-columns: 1fr; gap: 0; }
    .timeline-step { min-height: 0; padding: 1.25rem 0; text-align: left; border-right: 0; border-bottom: 1px solid rgba(148,163,184,.16); }
    .timeline-step:last-child { border-bottom: 0; }
    .timeline-step::after { top: auto; bottom: -.45rem; right: auto; left: 2rem; width: 1px; height: .9rem; }
    .timeline-step:last-child::after { display: none; }
    .timeline-step p { margin-left: 0; }
}
.nav-links { display: flex; align-items: center; gap: 1.35rem; margin-left: auto; margin-right: 1.5rem; }
.nav-links a { color: #aeb9d5; text-decoration: none; font-size: .72rem; letter-spacing: .04em; text-transform: none; transition: color .2s ease; }
.nav-links a:hover { color: #fff; }
.analysis-flow, .result-flow, .process-flow, .insight-flow, .technology-flow, .about-flow, .footer-wrap { scroll-margin-top: 7rem; }
.insight-flow, .technology-flow { margin-bottom: 5.5rem; }
.pipeline { display: flex; align-items: center; justify-content: space-between; gap: .7rem; margin-top: 2.2rem; }
.pipeline-node { display: flex; flex-direction: column; align-items: center; justify-content: center; min-width: 8rem; min-height: 5.2rem; padding: .65rem; color: #f8fafc; background: rgba(23, 31, 73, .78); border: 1px solid rgba(167,139,250,.48); border-radius: 18px; box-shadow: 0 0 22px rgba(124,92,255,.16); }
.pipeline-node span { color: #d8ccff; font-size: .72rem; font-weight: 800; letter-spacing: .08em; }
.pipeline-node small { color: #91a0c0; margin-top: .35rem; font-size: .68rem; }
.pipeline-connector { flex: 1; height: 1px; min-width: 1rem; background: linear-gradient(90deg, #8b5cf6, #60a5fa); box-shadow: 0 0 10px rgba(139,92,246,.7); }
.timeline { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0; margin-top: 2.2rem; }
.timeline-step { position: relative; min-height: 10rem; padding: 0 1.4rem; text-align: center; border-right: 1px solid rgba(148,163,184,.16); transition: transform .25s ease; }
.timeline-step:last-child { border-right: 0; }
.timeline-step::after { content: ''; position: absolute; top: 2.4rem; right: -.45rem; width: .9rem; height: 1px; background: #8b5cf6; box-shadow: 0 0 10px rgba(96,165,250,.7); }
.timeline-step:last-child::after { display: none; }
.timeline-step:hover { transform: translateY(-4px); }
.timeline-step:hover .timeline-icon { transform: scale(1.12); }
.timeline-step:hover .timeline-title { color: #d8ccff; }
.timeline-number { color: #c4b5fd; font-size: 1.25rem; font-weight: 800; letter-spacing: .08em; }
.timeline-icon { margin: .7rem 0; font-size: 1.25rem; transition: transform .25s ease; }
.timeline-title { color: #fff; font-size: .8rem; font-weight: 800; letter-spacing: .12em; transition: color .25s ease; }
.timeline-step p { margin: .6rem auto 0; max-width: 15rem; color: var(--muted) !important; font-size: .86rem; line-height: 1.55; }
.tech-pills { display: flex; flex-wrap: wrap; gap: .65rem; margin-top: 1.2rem; }
.tech-pills span { color: #d9d5ff; background: rgba(36, 43, 91, .68); border: 1px solid rgba(167,139,250,.28); border-radius: 999px; padding: .58rem .85rem; font-size: .78rem; }
.about-card { margin-top: 1.2rem; padding: 1.7rem 2rem; }
.about-card p { margin: 0 0 .75rem; }
.about-card p:last-child { margin-bottom: 0; }
.footer-wrap + div[data-testid="stExpander"] { width: 100%; max-width: 1200px; margin: 1rem auto 0; }
.footer-wrap + div[data-testid="stExpander"] summary { padding: .85rem 1rem; }
.team-list { display: grid; gap: .7rem; padding: .8rem .25rem .35rem; }
.team-member { display: flex; align-items: center; gap: .8rem; color: var(--muted-bright); font-size: .9rem; }
.team-avatar { display: inline-flex; align-items: center; justify-content: center; width: 2rem; height: 2rem; border-radius: 50%; color: #fff; font-size: .68rem; font-weight: 800; background: linear-gradient(135deg, #7c3aed, #2563eb); box-shadow: 0 0 16px rgba(124,92,255,.35); }
@media (max-width: 860px) {
    .dashboard-nav { flex-wrap: wrap; gap: .7rem; }
    .nav-links { order: 3; width: 100%; justify-content: center; margin: .25rem 0 0; gap: .8rem; }
    .nav-status { margin-left: auto; }
    .pipeline { flex-wrap: wrap; justify-content: center; }
    .pipeline-connector { flex: 0 0 2rem; }
}
@media (max-width: 560px) {
    .pipeline-connector { display: none; }
    .pipeline-node { flex: 1 1 7rem; min-width: 6.5rem; }
    .nav-links { gap: .45rem; justify-content: space-between; }
    .nav-links a { font-size: .64rem; }
    .about-card { padding: 1.3rem; }
}
/* Final layout and team presentation */
.dashboard-nav, .hero, .analysis-flow, .result-flow, .insight-flow,
.process-flow, .technology-flow, .about-flow, .footer-wrap,
.footer-wrap + div[data-testid="stExpander"], .about-flow + div[data-testid="stExpander"] {
    box-sizing: border-box;
    width: 100%;
    max-width: 1200px;
    margin-left: auto;
    margin-right: auto;
    padding-left: 32px;
    padding-right: 32px;
}
.process-flow { margin-top: 0; margin-bottom: 5.5rem; }
.process-flow .section-heading { margin-bottom: 0; }
.process-flow .section-copy { margin: 16px 0 42px; }
.timeline { margin-top: 0; }
.timeline-step { min-width: 0; }
div[data-testid="stExpander"] {
    box-sizing: border-box;
    background: rgba(12, 17, 43, .82) !important;
    border: 1px solid rgba(167, 139, 250, .28) !important;
    border-radius: 16px !important;
    padding: 0 !important;
    overflow: hidden;
}
div[data-testid="stExpander"] details,
div[data-testid="stExpander"] details[open],
div[data-testid="stExpander"] summary,
div[data-testid="stExpander"] summary:hover,
div[data-testid="stExpander"] summary:focus,
div[data-testid="stExpander"] summary:focus-visible {
    color: #f8fafc !important;
    background: rgba(12, 17, 43, .82) !important;
}
div[data-testid="stExpander"] summary {
    min-height: 3.1rem;
    padding: .85rem 1rem !important;
    outline: none !important;
}
div[data-testid="stExpander"] summary span,
div[data-testid="stExpander"] summary p,
div[data-testid="stExpander"] summary svg {
    color: #f8fafc !important;
    fill: #f8fafc !important;
}
div[data-testid="stExpander"] summary:hover span,
div[data-testid="stExpander"] summary:hover p,
div[data-testid="stExpander"] summary:hover svg {
    color: #d8ccff !important;
    fill: #d8ccff !important;
}
div[data-testid="stExpander"] > details > div {
    background: rgba(12, 17, 43, .72) !important;
    border-top: 1px solid rgba(148, 163, 184, .14);
    padding: .7rem 1rem 1rem !important;
}
.team-member { padding: .3rem .45rem; border-radius: 10px; transition: background .2s ease, transform .2s ease; }
.team-member:hover { background: rgba(124, 92, 255, .12); transform: translateX(4px); }
.footer-wrap { margin-top: 1.8rem; }
.footer-wrap + div[data-testid="stExpander"], .about-flow + div[data-testid="stExpander"] { margin-top: 0; margin-bottom: 1.8rem; }
@media (max-width: 720px) {
    .dashboard-nav, .hero, .analysis-flow, .result-flow, .insight-flow,
    .process-flow, .technology-flow, .about-flow, .footer-wrap,
    .footer-wrap + div[data-testid="stExpander"], .about-flow + div[data-testid="stExpander"] {
        padding-left: 32px;
        padding-right: 32px;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource
def load_model():
    model_path = os.path.join("models", "lstm_model.h5")
    if not os.path.exists(model_path):
        st.error(
            f"Model file not found:\n\n`{model_path}`\n\n"
            "Make sure your trained model is inside the delivery4/models folder."
        )
        st.stop()
    return tf.keras.models.load_model(model_path)


@st.cache_resource
def load_tokenizer():
    possible_paths = [
        os.path.join("models", "tokenizer.pkl"),
        os.path.join("models", "tokenizer.pickle"),
    ]
    possible_paths.extend(glob.glob(os.path.join("models", "*tokenizer*.pkl")))
    possible_paths.extend(glob.glob(os.path.join("models", "*tokenizer*.pickle")))
    tokenizer_path = None
    for path in possible_paths:
        if os.path.exists(path):
            tokenizer_path = path
            break
    if tokenizer_path is None:
        st.error(
            "Tokenizer file was not found inside the `models` folder.\n\n"
            "Expected something like `tokenizer.pkl`."
        )
        st.stop()
    with open(tokenizer_path, "rb") as file:
        tokenizer = pickle.load(file)
    return tokenizer


model = load_model()
tokenizer = load_tokenizer()

if "tweet_input" not in st.session_state:
    st.session_state.tweet_input = ""


st.markdown(
    """
<div class="ambient-orb orb-left"></div>
<div class="ambient-orb orb-right"></div>
<div class="dashboard-nav">
    <div class="brand-mark">🧠 Sentiment<span>AI</span></div>
    <div class="nav-links">
        <a href="#home">Home</a>
        <a href="#analyze">Analyze</a>
        <a href="#how-it-works">How It Works</a>
        <a href="#technology">Technology</a>
        <a href="#about">About</a>
    </div>
    <div class="nav-status">● SYSTEM READY</div>
</div>
<div id="home" class="hero">
    <div class="hero-kicker">Social intelligence, powered by deep learning</div>
    <h1 class="hero-title">🧠 <span class="gradient-text">Social Media Sentiment Intelligence</span></h1>
    <div class="hero-subtitle">AI-powered sentiment analysis using NLP, GloVe embeddings and LSTM deep learning.</div>
    <div class="hero-badge">⚡ AI <span>•</span> NLP <span>•</span> LSTM</div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('<div id="analyze" class="analysis-flow">', unsafe_allow_html=True)
st.markdown(
    """
<div class="input-card">
    <div class="card-eyebrow">Analysis workspace</div>
    <div class="input-heading">Analyze Social Media Text</div>
    <div class="input-description">Enter a tweet or social media message and let the trained LSTM model analyze its sentiment.</div>
""",
    unsafe_allow_html=True,
)

tweet = st.text_area(
    "Tweet",
    value=st.session_state.tweet_input,
    height=155,
    placeholder="Example: I absolutely love this product! The experience was amazing.",
    label_visibility="collapsed",
    key="tweet_text_area",
)
if tweet:
    st.markdown(f'<div class="meta-line">{len(tweet)} characters</div>', unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

analyze = st.button("🔍 Analyze Sentiment", type="primary", key="analyze_button")
st.markdown("</div>", unsafe_allow_html=True)


if analyze:
    if not tweet.strip():
        st.warning("⚠️ Please enter a tweet or social media message first.")
    else:
        with st.spinner("🧠 Analyzing your text..."):
            sequence = tokenizer.texts_to_sequences([tweet])
            padded_sequence = tf.keras.preprocessing.sequence.pad_sequences(
                sequence,
                maxlen=30,
            )
            prediction = model.predict(padded_sequence, verbose=0)
            score = float(prediction[0][0])

        if score >= 0.5:
            sentiment = "Positive"
            emoji = "😊"
            confidence = score * 100
        else:
            sentiment = "Negative"
            emoji = "😞"
            confidence = (1 - score) * 100

        sentiment_class = sentiment.lower()
        st.markdown('<div class="result-flow">', unsafe_allow_html=True)
        st.markdown(
            f"""
<div class="result-shell">
    <div class="result-label">SENTIMENT RESULT</div>
    <div class="result-sentiment {sentiment_class}">{emoji} {sentiment} Sentiment</div>
    <p class="section-copy">The trained model has evaluated the emotional tone of your text.</p>
    <div class="card-eyebrow">Signal metrics</div>
""",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
    <div class="result-metrics">
        <div class="metric-card"><div class="metric-name">Prediction Score</div><div class="metric-value">{score:.4f}</div></div>
        <div class="metric-card"><div class="metric-name">Confidence</div><div class="metric-value">{confidence:.2f}%</div></div>
        <div class="metric-card"><div class="metric-name">Prediction</div><div class="metric-value">{emoji} {sentiment}</div></div>
    </div>
    <div class="metric-name" style="margin-top:1.8rem;">MODEL CONFIDENCE</div>
    <div class="confidence-track"><div class="confidence-fill" style="width:{min(max(confidence, 0), 100):.2f}%;"></div></div>
    <div class="confidence-copy">{confidence:.2f}% confidence in this classification</div>
</div>
""",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)


st.markdown(
    """
<div class="insight-flow">
    <div class="section-heading">🧠 What the AI Sees</div>
    <div class="section-copy">From words to sentiment — the model transforms social media language into a numerical representation before making a prediction.</div>
    <div class="pipeline">
        <div class="pipeline-node"><span>TEXT</span><small>raw language</small></div>
        <div class="pipeline-connector"></div>
        <div class="pipeline-node"><span>TOKENIZATION</span><small>sequence IDs</small></div>
        <div class="pipeline-connector"></div>
        <div class="pipeline-node"><span>GloVe</span><small>embeddings</small></div>
        <div class="pipeline-connector"></div>
        <div class="pipeline-node"><span>LSTM</span><small>context</small></div>
        <div class="pipeline-connector"></div>
        <div class="pipeline-node"><span>SCORE</span><small>sentiment</small></div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('<div id="how-it-works" class="process-flow"><div class="section-heading">How It Works</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-copy">From raw social text to an actionable sentiment signal.</div>',
    unsafe_allow_html=True,
)
steps = [
    ("01", "📝", "INPUT", "Social media text enters the analysis pipeline."),
    ("02", "🔤", "REPRESENTATION", "Words are converted into numerical representations using GloVe embeddings."),
    ("03", "🧠", "LSTM ANALYSIS", "The LSTM model learns contextual patterns in the text."),
    ("04", "📊", "PREDICTION", "The model generates a sentiment score and classification."),
]
timeline_html = '<div class="timeline">'
for number, icon, title, copy in steps:
    timeline_html += (
        f'<div class="timeline-step"><div class="timeline-number">{number}</div>'
        f'<div class="timeline-icon">{icon}</div><div class="timeline-title">{title}</div>'
        f'<p>{copy}</p></div>'
    )
timeline_html += "</div>"
st.markdown(timeline_html, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
<div id="technology" class="technology-flow">
    <div class="section-heading">⚙️ Technology Stack</div>
    <div class="tech-pills">
        <span>Python</span><span>TensorFlow / Keras</span><span>LSTM</span><span>NLP</span>
        <span>GloVe</span><span>NumPy</span><span>Pandas</span><span>Streamlit</span>
    </div>
</div>
<div id="about" class="about-flow">
    <div class="section-heading">ℹ️ About This Project</div>
    <div class="about-card">
        <p>This project uses Natural Language Processing, GloVe word embeddings and an LSTM deep learning model to classify social media text as positive or negative.</p>
        <p>The model converts text into sequences, represents words numerically and uses LSTM to capture contextual patterns before producing a sentiment score.</p>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

with st.expander("👥  Meet the Team"):
    st.markdown(
        """
<div class="team-list">
    <div class="team-member"><span class="team-avatar">RP</span><span>Rupesh Patil</span></div>
    <div class="team-member"><span class="team-avatar">VS</span><span>Vishal Sahane</span></div>
    <div class="team-member"><span class="team-avatar">ON</span><span>Om Nikumbh</span></div>
    <div class="team-member"><span class="team-avatar">KP</span><span>Kaustubh Patil</span></div>
</div>
""",
        unsafe_allow_html=True,
    )

st.markdown(
    """
<div class="footer-wrap">
    <div class="footer-name">Social Media Sentiment Intelligence</div>
    <div class="footer-copy">Built as a Team Project • 2026<br>Developed collaboratively by the team.</div>
</div>
""",
    unsafe_allow_html=True,
)
 
