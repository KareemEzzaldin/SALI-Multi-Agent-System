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
    if (el.topbarMastery) el.topbarMastery.textContent = `${pct}%`;
    if (el.topbarStability) el.topbarStability.textContent = `${currentConcept.stability}d`;

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
        ⚡ تجربة خطأ شائع: "${p.title}"
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
    const isEnglish = currentCourse && currentCourse.course_id === 'ENG-501';
    const qText = sampleQ ? sampleQ.question_text : `يلا بينا نتدرب على مفهوم ${currentConcept.concept_name}`;
    const options = sampleQ?.options || [];

    let optionsHtml = '';
    if (options.length > 0) {
      optionsHtml = `
        <div class="mcq-options-grid">
          ${options.map(opt => `
            <button type="button" class="mcq-option-btn" data-choice="${opt.key}" data-text="${encodeURIComponent(opt.text)}">
              <span class="mcq-key-pill">${opt.key}</span>
              <span class="mcq-text-content ${isEnglish ? 'ltr-text' : 'rtl-text'}">${opt.text}</span>
            </button>
          `).join('')}
        </div>
      `;
    }

    const greetingHeading = isEnglish
      ? `أهلاً بك يا بطل! 👋 يلا نتدرب على <strong>${currentConcept.concept_name}</strong>`
      : `أهلاً بك يا بطل! 👋 يلا نتدرب على درس <strong>${currentConcept.concept_name}</strong>`;

    const instructionsText = options.length > 0
      ? 'اضغط على الاختيار المناسب مباشرة أو اكتب إجابتك بالأسفل:'
      : 'اكتب إجابتك أو طريقتك في الحل في المربع بالأسفل:';

    const initialContent = `
      <p style="font-weight: 600; font-size: 0.98rem; color: #f8fafc; margin-bottom: 0.35rem; direction: rtl; text-align: right;">
        أهلاً بك يا بطل! 👋 يلا نتدرب على <span dir="auto" style="color: var(--accent-cyan); font-weight: 700;">${currentConcept.concept_name}</span>
      </p>
      <p style="color: #cbd5e1; font-size: 0.88rem; margin-bottom: 0.6rem; direction: rtl; text-align: right;">
        ${instructionsText}
      </p>
      <div style="background: rgba(0,0,0,0.32); border-radius: 8px; padding: 0.95rem; margin: 0.5rem 0; border-left: 4px solid var(--accent-cyan);">
        <div class="${isEnglish ? 'ltr-text' : 'rtl-text'}" style="font-size: 1.02rem; font-weight: 600; line-height: 1.5; color: #f1f5f9;">
          ${qText.replace(/\n/g, '<br>')}
        </div>
        ${optionsHtml}
      </div>
      <p style="font-size: 0.8rem; color: #94a3b8; margin-top: 0.4rem; direction: rtl; text-align: right;">
        💡 ${options.length > 0 ? 'تقدر تضغط على الزر للإجابة فوراً، أو تكتبها بإيدك بالطريقة اللي تريحك!' : 'اكتب إجابتك وسيقوم المعلم الذكي بمراجعتها فوراً!'}
      </p>
    `;

    const msgRow = appendMessage('tutor', initialContent, 'practice-mode', null);
    attachMcqClickHandlers(msgRow);
  }

  function attachMcqClickHandlers(container) {
    if (!container) return;
    const btns = container.querySelectorAll('.mcq-option-btn');
    btns.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const choiceKey = btn.getAttribute('data-choice');
        const choiceText = decodeURIComponent(btn.getAttribute('data-text') || '');
        
        // Show choice in input and send
        el.chatInputText.value = `${choiceKey} - ${choiceText}`;
        handleSendMessage();

        // Visually mark selected and disable group
        btns.forEach(b => {
          b.disabled = true;
          b.style.opacity = b === btn ? '1' : '0.45';
          b.style.borderColor = b === btn ? 'var(--accent-indigo)' : 'transparent';
          b.style.pointerEvents = 'none';
        });
      });
    });
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
      appendMessage('tutor', `<p style="color: #f43f5e;">⚠️ حدث خطأ في التواصل مع المعلم الذكي. يرجى التأكد من تشغيل السيرفر على منفذ 8000.</p>`, 'escalation-mode', null);
    }
  }

  async function handleAskAdaptiveQuestion() {
    appendMessage('student', '🎲 هل يمكنك إعطائي سؤال تدريبي تكيفي جديد؟', '', null);
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

      const isEnglish = currentCourse && currentCourse.course_id === 'ENG-501';
      const options = item.options || [];
      const optionsHtml = options.map(o => `
        <button type="button" class="mcq-option-btn" data-choice="${o.key}" data-text="${encodeURIComponent(o.text)}">
          <span class="mcq-key-pill">${o.key}</span>
          <span class="mcq-text-content ${isEnglish ? 'ltr-text' : 'rtl-text'}">${o.text}</span>
        </button>
      `).join('');

      const content = `
        <p style="font-weight: 600; color: #f8fafc; margin-bottom: 0.35rem;">🎯 <strong>سؤال تدريبي جديد:</strong></p>
        <div style="background: rgba(0,0,0,0.32); border-radius: 8px; padding: 0.95rem; margin: 0.5rem 0; border-left: 4px solid var(--accent-indigo);">
          <div class="${isEnglish ? 'ltr-text' : 'rtl-text'}" style="font-size: 1.02rem; font-weight: 600; line-height: 1.5; color: #f1f5f9;">
            ${item.question_text.replace(/\n/g, '<br>')}
          </div>
          ${options.length > 0 ? `<div class="mcq-options-grid">${optionsHtml}</div>` : ''}
        </div>
        <p style="font-size: 0.8rem; color: #94a3b8; margin-top: 0.4rem;">اضغط على الاختيار المناسب أو اكتب إجابتك بالأسفل!</p>
      `;

      const msgRow = appendMessage('tutor', content, 'practice-mode', null);
      attachMcqClickHandlers(msgRow);

    } catch (e) {
      typingRow.remove();
      console.error(e);
      appendMessage('tutor', 'تعذر توليد سؤال جديد حالياً. يمكنك تجربة اختيار المفهوم مرة أخرى.', 'escalation-mode', null);
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

    const hasArabic = /[\u0600-\u06FF]/.test(htmlContent);
    const dirClass = hasArabic ? 'rtl-bubble' : 'ltr-bubble';

    const bubble = document.createElement('div');
    bubble.className = `msg-bubble ${modeClass} ${dirClass}`;
    bubble.innerHTML = htmlContent;

    // Append subtle source badge and collapsed teacher telemetry if agentData exists
    if (agentData) {
      const citations = agentData.grounding?.citations || [];
      if (citations.length > 0) {
        const c = citations[0];
        const badge = document.createElement('div');
        badge.className = 'grounded-source-badge';
        badge.innerHTML = `📖 المرجع المعتمد: ${c.source_file || 'كتاب الوزارة'} ${c.page_or_slide_number ? `(صـ ${c.page_or_slide_number})` : ''}`;
        bubble.appendChild(badge);
      }

      // Collapsible Teacher Telemetry Details
      const accordion = document.createElement('div');
      accordion.className = 'simple-teacher-accordion';
      
      const toggleBtn = document.createElement('button');
      toggleBtn.type = 'button';
      toggleBtn.className = 'simple-teacher-toggle';
      toggleBtn.innerHTML = `
        <span>⚙️ تفاصيل التقييم الذكي للمعلم</span>
        <span class="toggle-arrow">▼</span>
      `;

      const delta = agentData.state_update.mastery_delta || 0;
      const deltaSign = delta >= 0 ? '+' : '';
      const detailBox = document.createElement('div');
      detailBox.className = 'telemetry-detail-box';
      detailBox.style.display = 'none';
      detailBox.style.marginTop = '0.5rem';
      detailBox.innerHTML = `
        <p><strong>🎯 تشخيص الفهم:</strong> <span style="color: ${agentData.is_correct ? '#10b981' : '#f59e0b'}; font-weight: 600;">${agentData.is_correct ? 'إجابة صحيحة ومتقنة' : (agentData.misconception.description || 'بحاجة لتصويب وتوضيح')}</span></p>
        <p><strong>📊 نسبة الإتقان (BKT):</strong> ${Math.round(agentData.state_update.new_mastery * 100)}% (تغيير: <span style="color:${delta >= 0 ? '#10b981' : '#f43f5e'}">${deltaSign}${Math.round(delta * 100)}%</span>)</p>
        <p><strong>🧠 استقرار الذاكرة:</strong> ${agentData.state_update.memory_stability_days} أيام (منحنى إبنجهاوس)</p>
        <p><strong>🧭 الإجراء التربوي:</strong> ${agentData.action_type}</p>
        <p style="font-size: 0.76rem; color: #94a3b8; margin-top: 0.3rem;">${agentData.reasoning}</p>
      `;

      toggleBtn.addEventListener('click', () => {
        const isHidden = detailBox.style.display === 'none';
        detailBox.style.display = isHidden ? 'block' : 'none';
        toggleBtn.querySelector('.toggle-arrow').textContent = isHidden ? '▲' : '▼';
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
        <span style="animation: pulseGlow 1.5s infinite;">🧠 جاري التقييم بواسطة المعلم الذكي...</span>
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
