/**
 * SALI AI Tutor & Student Cognitive Twin Chat Portal
 * Orchestrates conversational AI Tutor interactions with the 5 AI Agents.
 */

(function () {
  'use strict';

  const API_BASE = window.location.origin;

  let studentProfile = {
    name: 'Kareem Ezzaldin',
    student_id: 'STD-2026-904'
  };

  let coursesData = [];
  let currentCourse = null;
  let currentConcept = null;
  let consecutiveFailures = 0;
  let attemptNumber = 1;

  // DOM Elements
  const el = {
    courseDropdown: document.getElementById('courseDropdown'),
    conceptsStack: document.getElementById('conceptsStack'),
    btnAskAdaptiveQ: document.getElementById('btnAskAdaptiveQ'),
    btnClearChat: document.getElementById('btnClearChat'),
    chatActiveTopic: document.getElementById('chatActiveTopic'),
    chatActiveCourseName: document.getElementById('chatActiveCourseName'),
    topbarMastery: document.getElementById('topbarMastery'),
    topbarStability: document.getElementById('topbarStability'),
    chatMessagesScroll: document.getElementById('chatMessagesScroll'),
    chatQuickChips: document.getElementById('chatQuickChips'),
    chipsContainer: document.getElementById('chipsContainer'),
    chatInputText: document.getElementById('chatInputText'),
    btnSendMessage: document.getElementById('btnSendMessage')
  };

  // ─────────────────────────────────────────────
  // INITIALIZATION
  // ─────────────────────────────────────────────

  async function init() {
    setupEventListeners();
    await fetchCourses();
    renderCourseDropdown();
    selectCourse(coursesData[0].course_id);
  }

  async function fetchCourses() {
    try {
      const res = await fetch(`${API_BASE}/api/courses`);
      if (res.ok) {
        coursesData = await res.json();
      } else {
        throw new Error('Courses API error');
      }
    } catch (e) {
      console.warn('Using client fallback course data:', e);
      coursesData = getFallbackCourses();
    }
  }

  function setupEventListeners() {
    el.courseDropdown.addEventListener('change', (e) => {
      selectCourse(e.target.value);
    });

    el.btnSendMessage.addEventListener('click', handleSendMessage);

    el.chatInputText.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSendMessage();
      }
    });

    el.btnAskAdaptiveQ.addEventListener('click', handleAskAdaptiveQuestion);
    el.btnClearChat.addEventListener('click', handleClearChat);
  }

  // ─────────────────────────────────────────────
  // COURSE & CONCEPT MANAGEMENT
  // ─────────────────────────────────────────────

  function renderCourseDropdown() {
    el.courseDropdown.innerHTML = coursesData.map(c => 
      `<option value="${c.course_id}">${c.code} — ${c.course_title}</option>`
    ).join('');
  }

  function selectCourse(courseId) {
    currentCourse = coursesData.find(c => c.course_id === courseId) || coursesData[0];
    el.chatActiveCourseName.textContent = currentCourse.course_title;
    renderConceptsStack();
    selectConcept(currentCourse.concepts[0].concept_id);
  }

  function renderConceptsStack() {
    el.conceptsStack.innerHTML = currentCourse.concepts.map(c => `
      <div class="concept-card ${currentConcept && currentConcept.concept_id === c.concept_id ? 'active' : ''}" 
           data-id="${c.concept_id}">
        <div class="concept-card-title-row">
          <span class="concept-title">${c.concept_name}</span>
          <span class="concept-pct" id="pct-${c.concept_id}">${Math.round(c.mastery * 100)}%</span>
        </div>
        <div class="concept-bar-track">
          <div class="concept-bar-fill" id="bar-${c.concept_id}" style="width: ${Math.round(c.mastery * 100)}%"></div>
        </div>
      </div>
    `).join('');

    el.conceptsStack.querySelectorAll('.concept-card').forEach(card => {
      card.addEventListener('click', () => {
        selectConcept(card.getAttribute('data-id'));
      });
    });
  }

  function selectConcept(conceptId) {
    currentConcept = currentCourse.concepts.find(c => c.concept_id === conceptId) || currentCourse.concepts[0];
    consecutiveFailures = 0;
    attemptNumber = 1;

    // Update active highlight
    el.conceptsStack.querySelectorAll('.concept-card').forEach(c => {
      c.classList.toggle('active', c.getAttribute('data-id') === currentConcept.concept_id);
    });

    el.chatActiveTopic.textContent = currentConcept.concept_name;
    updateTopbarTelemetry();
    renderQuickMisconceptionChips();

    // Clear and post initial greeting
    el.chatMessagesScroll.innerHTML = '';
    postInitialTutorGreeting();
  }

  function updateTopbarTelemetry() {
    const pct = Math.round(currentConcept.mastery * 100);
    el.topbarMastery.textContent = `${pct}%`;
    el.topbarStability.textContent = `${currentConcept.stability}d`;

    const pctEl = document.getElementById(`pct-${currentConcept.concept_id}`);
    const barEl = document.getElementById(`bar-${currentConcept.concept_id}`);
    if (pctEl) pctEl.textContent = `${pct}%`;
    if (barEl) barEl.style.width = `${pct}%`;
  }

  function renderQuickMisconceptionChips() {
    const presets = currentConcept.sample_question?.misconception_presets || [];
    if (presets.length === 0) {
      el.chatQuickChips.style.display = 'none';
      return;
    }

    el.chatQuickChips.style.display = 'flex';
    el.chipsContainer.innerHTML = presets.map((p, idx) => `
      <button class="chip-test-btn" data-answer="${encodeURIComponent(p.answer)}">
        ⚡ Test: "${p.title}"
      </button>
    `).join('');

    el.chipsContainer.querySelectorAll('.chip-test-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const text = decodeURIComponent(btn.getAttribute('data-answer'));
        el.chatInputText.value = text;
        handleSendMessage();
      });
    });
  }

  // ─────────────────────────────────────────────
  // CONVERSATIONAL CHAT LOGIC
  // ─────────────────────────────────────────────

  function postInitialTutorGreeting() {
    const sampleQ = currentConcept.sample_question;
    const qText = sampleQ ? sampleQ.question_text : `ما رأيك أن نتحدث عن مفهوم ${currentConcept.concept_name}؟`;

    const initialContent = `
      <p>أهلاً يا بطل! 👋 جاهز نتدرب على <strong>${currentConcept.concept_name}</strong>؟</p>
      <p style="margin-top: 0.4rem;">إليك هذا السؤال لاختبار فهمك ومعايرة توأمك المعرفي:</p>
      <div style="background: rgba(0,0,0,0.3); border-radius: 8px; padding: 0.8rem; margin: 0.6rem 0; border-left: 3px solid var(--accent-cyan); font-weight: 500;">
        ${qText.replace(/\n/g, '<br>')}
      </div>
      <p style="font-size: 0.85rem; color: #94a3b8;">اكتب إجابتك أو فكرتك، أو اضغط على أحد شرائح الأخطاء الشائعة بالأعلى لتجربة رد الذكاء الاصطناعي!</p>
    `;

    appendMessage('tutor', initialContent, 'practice-mode', null);
  }


  async function handleSendMessage() {
    const text = el.chatInputText.value.trim();
    if (!text) return;

    // Render Student Message
    appendMessage('student', text, '', null);
    el.chatInputText.value = '';
    el.chatInputText.focus();

    // Show typing placeholder
    const typingRow = appendTypingIndicator();

    try {
      const payload = {
        learner_id: studentProfile.student_id,
        course_id: currentCourse.course_id,
        concept_id: currentConcept.concept_id,
        student_message: text,
        consecutive_failures: consecutiveFailures,
        attempt_number: attemptNumber
      };

      const res = await fetch(`${API_BASE}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error(`Server returned ${res.status}`);
      const data = await res.json();

      typingRow.remove();

      // Update counters
      attemptNumber++;
      if (!data.is_correct) {
        consecutiveFailures++;
      } else {
        consecutiveFailures = 0;
      }

      // Update concept mastery locally
      currentConcept.mastery = data.state_update.new_mastery;
      currentConcept.stability = data.state_update.memory_stability_days;
      updateTopbarTelemetry();

      // Render Tutor Reply
      let modeClass = 'practice-mode';
      if (data.action_type === 'socratic_tutoring') modeClass = 'socratic-mode';
      else if (data.action_type === 'remediation') modeClass = 'remediation-mode';
      else if (data.action_type === 'escalation') modeClass = 'escalation-mode';

      appendMessage('tutor', data.tutor_reply.replace(/\n/g, '<br>'), modeClass, data);

    } catch (err) {
      typingRow.remove();
      console.error('Chat error:', err);
      appendMessage('tutor', `<p style="color: #f43f5e;">⚠️ Error communicating with AI Agents. Please ensure the backend server is running on port 8000.</p>`, 'escalation-mode', null);
    }
  }

  async function handleAskAdaptiveQuestion() {
    appendMessage('student', '🎲 Could you give me an adaptive question in my Zone of Proximal Development?', '', null);
    const typingRow = appendTypingIndicator();

    try {
      const res = await fetch(`${API_BASE}/api/chat/generate-question`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          learner_id: studentProfile.student_id,
          course_id: currentCourse.course_id,
          concept_id: currentConcept.concept_id,
          student_message: 'request_adaptive_question'
        })
      });

      if (!res.ok) throw new Error('Adaptive question endpoint error');
      const item = await res.json();

      typingRow.remove();

      const optionsHtml = item.options.map(o => `
        <div style="margin: 0.35rem 0; padding: 0.4rem 0.6rem; background: rgba(255,255,255,0.03); border-radius: 6px; border: 1px solid rgba(255,255,255,0.06);">
          <strong>${o.key}:</strong> ${o.text}
        </div>
      `).join('');

      const content = `
        <p>🎯 <strong>Adaptive Question (Agent 3 - ZPD)</strong></p>
        <div style="display: flex; gap: 0.5rem; margin: 0.4rem 0;">
          <span style="font-size: 0.7rem; padding: 0.15rem 0.5rem; border-radius: 99px; background: rgba(139, 92, 246, 0.2); color: #c4b5fd;">Bloom: ${item.bloom_level}</span>
          <span style="font-size: 0.7rem; padding: 0.15rem 0.5rem; border-radius: 99px; background: rgba(6, 182, 212, 0.2); color: #67e8f9;">Difficulty: ${item.difficulty}</span>
        </div>
        <p style="margin-top: 0.4rem; font-weight: 500;">${item.question_text}</p>
        ${item.code_snippet ? `<pre><code>${item.code_snippet}</code></pre>` : ''}
        <div style="margin-top: 0.5rem;">${optionsHtml}</div>
        <p style="font-size: 0.8rem; color: #94a3b8; margin-top: 0.4rem;">Type your answer or selection below!</p>
      `;

      appendMessage('tutor', content, 'practice-mode', null);

    } catch (e) {
      typingRow.remove();
      console.error(e);
      appendMessage('tutor', 'Could not generate an adaptive question at this moment.', 'escalation-mode', null);
    }
  }

  function handleClearChat() {
    el.chatMessagesScroll.innerHTML = '';
    consecutiveFailures = 0;
    attemptNumber = 1;
    postInitialTutorGreeting();
  }

  // ─────────────────────────────────────────────
  // DOM MESSAGE HELPERS
  // ─────────────────────────────────────────────

  function appendMessage(sender, htmlContent, modeClass, agentData) {
    const row = document.createElement('div');
    row.className = `chat-msg-row ${sender}`;

    const avatar = document.createElement('div');
    avatar.className = 'msg-avatar';
    avatar.textContent = sender === 'student' ? 'KE' : 'AI';

    const bubble = document.createElement('div');
    bubble.className = `msg-bubble ${modeClass}`;
    bubble.innerHTML = htmlContent;

    // Append collapsible agent telemetry drawer if agent data exists
    if (agentData) {
      const accordion = document.createElement('div');
      accordion.className = 'agent-telemetry-accordion';

      const toggleBtn = document.createElement('button');
      toggleBtn.className = 'telemetry-summary-btn';
      const groundingCitations = agentData.grounding?.citations || [];
      const hasCitations = groundingCitations.length > 0;
      const groundingPct = Math.round((agentData.grounding?.confidence || 0.9) * 100);

      toggleBtn.innerHTML = `
        <span>🔍 Multi-Agent Telemetry:</span>
        <strong style="color: ${agentData.misconception.detected ? '#f59e0b' : '#10b981'};">
          ${agentData.misconception.detected ? 'Misconception Detected' : 'Clear'}
        </strong>
        <span style="color: #38bdf8;">• 📚 Grounded ${groundingPct}%</span>
        <span>• Action: ${agentData.action_type}</span>
        <span>▼</span>
      `;

      const citationsHtml = hasCitations ? `
        <div style="margin-top: 0.3rem;">
          <strong style="color: #38bdf8;">📚 Verified Course Citations (AI #1):</strong>
          <ul style="margin: 0.25rem 0 0.4rem 1.1rem; font-size: 0.75rem; color: #cbd5e1; list-style: disc;">
            ${groundingCitations.map(c => `
              <li style="margin-bottom: 0.2rem;">
                <span style="color: #67e8f9; font-weight: 600;">${c.citation_id}</span> 
                <strong>${c.source_file}</strong> ${c.page_or_slide_number ? `(Slide/p. ${c.page_or_slide_number})` : ''}: 
                <span style="color: #94a3b8; font-style: italic;">"${c.quoted_snippet}"</span>
              </li>
            `).join('')}
          </ul>
        </div>
      ` : '';

      const nextStepsHtml = agentData.grounding?.next_steps?.length > 0 ? `
        <p style="font-size: 0.75rem; color: #c084fc; margin-top: 0.3rem;">
          <strong>🧭 DAG Next Study Path:</strong> ${agentData.grounding.next_steps.join(' ➔ ')}
        </p>
      ` : '';

      const detailBox = document.createElement('div');
      detailBox.className = 'telemetry-detail-box';
      detailBox.innerHTML = `
        <p><strong>AI #1 Grounding:</strong> Confidence: <span style="color: #38bdf8; font-weight: 600;">${groundingPct}%</span> (${agentData.grounding?.model_used || 'Claude 3.5 Sonnet Grounded'})</p>
        ${citationsHtml}
        ${nextStepsHtml}
        <div style="margin-top: 0.4rem; padding-top: 0.35rem; border-top: 1px dashed rgba(255,255,255,0.1);">
          <p><strong>Agent 1 (BKT):</strong> Mastery delta: <span style="color:${agentData.state_update.mastery_delta >= 0 ? '#10b981' : '#f43f5e'}">${agentData.state_update.mastery_delta >= 0 ? '+' : ''}${agentData.state_update.mastery_delta}</span> | Stability: ${agentData.state_update.memory_stability_days}d</p>
          <p><strong>Agent 2 (Misconception):</strong> ${agentData.misconception.detected ? agentData.misconception.description : 'No misconception pattern identified.'}</p>
          <p><strong>Agent 4 (Pedagogical Rule):</strong> ${agentData.reasoning}</p>
          ${agentData.human_dossier ? `<p style="color: #f43f5e;"><strong>🚨 Agent 5 Escalation Dossier:</strong> Urgency ${agentData.human_dossier.urgency} — Mentor notified.</p>` : ''}
        </div>
      `;


      toggleBtn.addEventListener('click', () => {
        const isHidden = detailBox.style.display === 'none' || !detailBox.style.display;
        detailBox.style.display = isHidden ? 'block' : 'none';
        toggleBtn.querySelector('span:last-child').textContent = isHidden ? '▲' : '▼';
      });

      accordion.appendChild(toggleBtn);
      accordion.appendChild(detailBox);
      bubble.appendChild(accordion);
    }

    row.appendChild(avatar);
    row.appendChild(bubble);
    el.chatMessagesScroll.appendChild(row);

    // Auto-scroll
    el.chatMessagesScroll.scrollTop = el.chatMessagesScroll.scrollHeight;
    return row;
  }

  function appendTypingIndicator() {
    const row = document.createElement('div');
    row.className = 'chat-msg-row tutor';
    row.innerHTML = `
      <div class="msg-avatar">AI</div>
      <div class="msg-bubble" style="color: var(--text-muted); font-style: italic; display: flex; align-items: center; gap: 0.4rem;">
        <span style="animation: pulseGlow 1.5s infinite;">🧠 جاري التحليل عبر وكلاء الذكاء الاصطناعي (AI Agents Evaluating)...</span>
      </div>
    `;
    el.chatMessagesScroll.appendChild(row);
    el.chatMessagesScroll.scrollTop = el.chatMessagesScroll.scrollHeight;
    return row;
  }

  // ─────────────────────────────────────────────
  // FALLBACK DATA (PRIMARY 5)
  // ─────────────────────────────────────────────

  function getFallbackCourses() {
    return [
      {
        course_id: "ENG-501",
        course_title: "English — Connect 5 (Primary 5)",
        code: "ENG-501",
        concepts: [
          {
            concept_id: "c_past_simple",
            concept_name: "Past Simple & Irregular Verbs",
            mastery: 0.40,
            stability: 2.2,
            sample_question: {
              question_text: "Yesterday, my family and I ______ to Alexandria and we ______ the Qaitbay Citadel.",
              misconception_presets: [
                { title: "Over-regularization ('goed')", answer: "We goed to Alexandria and visited the Citadel" }
              ]
            }
          }
        ]
      },
      {
        course_id: "MATH-501",
        course_title: "الرياضيات — الصف الخامس الابتدائي",
        code: "MATH-501",
        concepts: [
          {
            concept_id: "c_decimals_place_value",
            concept_name: "الكسور العشرية والقيمة المكانية حتى الجزء من ألف",
            mastery: 0.35,
            stability: 2.0,
            sample_question: {
              question_text: "قارن بين العددين العشريين: 0.8 و 0.25 مستخدماً (> أو < أو =).",
              misconception_presets: [
                { title: "مغالطة مقارنة العدد الصحيح", answer: "0.25 أكبر من 0.8 لأن 25 أكبر من 8" }
              ]
            }
          }
        ]
      }
    ];
  }


  window.addEventListener('DOMContentLoaded', init);

})();
