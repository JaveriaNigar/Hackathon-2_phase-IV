// frontend/src/components/CursorEffectWrapper.tsx
'use client';

import { useEffect } from 'react';
import { initCursorGlowEffects } from '@/lib/cursor-effects';

export default function CursorEffectWrapper({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    // Initialize cursor glow effects when component mounts
    const cleanup = initCursorGlowEffects();
    
    // Reinitialize on any dynamic content updates
    const mutationObserver = new MutationObserver(() => {
      // Small delay to ensure DOM is updated
      setTimeout(initCursorGlowEffects, 0);
    });
    
    mutationObserver.observe(document.body, {
      childList: true,
      subtree: true
    });
    
    // Cleanup function
    return () => {
      cleanup();
      mutationObserver.disconnect();
    };
  }, []);

  return <>{children}</>;
}