import { createClient } from '@supabase/supabase-js';

const supabaseUrl = 'https://usmocjdkwcyqbsfavduy.supabase.co';
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVzbW9jamRrd2N5cWJzZmF2ZHV5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODE1MDUwODksImV4cCI6MjA5NzA4MTA4OX0.OcMOuKKA8s8NjdVRNx_ciCNo51Ax9Rf0A-pXEUqXqSQ';

export const supabase = createClient(supabaseUrl, supabaseAnonKey);