// User types
export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
  is_staff: boolean;
  date_joined: string;
  last_login: string;
}

// Tenant types
export interface Tenant {
  id: string;
  name: string;
  schema_name: string;
  domain?: string;
  subdomain?: string;
  is_active: boolean;
  is_verified: boolean;
  is_premium: boolean;
  plan_type: 'free' | 'basic' | 'pro' | 'enterprise';
  product_limit: number;
  order_limit: number;
  storage_limit_mb: number;
  contact_email?: string;
  contact_phone?: string;
  contact_address?: string;
  created_at: string;
  updated_at: string;
  trial_ends_at?: string;
  subscription_ends_at?: string;
}

// Storefront types
export interface Storefront {
  id: string;
  tenant: string;
  store_name: string;
  store_description?: string;
  store_tagline?: string;
  logo_url?: string;
  favicon_url?: string;
  hero_image_url?: string;
  contact_email?: string;
  contact_phone?: string;
  contact_address?: string;
  business_hours: Record<string, unknown>;
  social_links: Record<string, unknown>;
  meta_title?: string;
  meta_description?: string;
  meta_keywords?: string;
  og_image_url?: string;
  google_analytics_id?: string;
  facebook_pixel_id?: string;
  google_tag_manager_id?: string;
  is_active: boolean;
  is_published: boolean;
  published_at?: string;
  created_at: string;
  updated_at: string;
}

// Theme types
export interface Theme {
  id: string;
  storefront: string;
  primary_color: string;
  secondary_color: string;
  accent_color: string;
  background_color: string;
  text_color: string;
  link_color: string;
  success_color: string;
  warning_color: string;
  error_color: string;
  font_family: string;
  heading_font_family: string;
  font_size_base: string;
  line_height_base: number;
  layout_type: 'grid' | 'list' | 'masonry' | 'carousel';
  container_width: string;
  sidebar_position: 'left' | 'right' | 'none';
  spacing_unit: string;
  border_radius: string;
  box_shadow: string;
  custom_css?: string;
  custom_js?: string;
  created_at: string;
  updated_at: string;
}

// Product types
export interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  stock: number;
  image_url?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

// Order types
export interface Order {
  id: string;
  order_number: string;
  customer_name: string;
  customer_email: string;
  total_amount: number;
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled';
  created_at: string;
  updated_at: string;
  items: OrderItem[];
}

export interface OrderItem {
  id: string;
  order: string;
  product: Product;
  quantity: number;
  price: number;
}

// API Response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

export interface PaginatedResponse<T> {
  count: number;
  next?: string;
  previous?: string;
  results: T[];
}

// Dashboard statistics
export interface DashboardStats {
  total_tenants: number;
  total_storefronts: number;
  total_products: number;
  total_orders: number;
  total_revenue: number;
  recent_orders: Order[];
  top_products: Product[];
}

// Form types
export interface LoginForm {
  email: string;
  password: string;
}

export interface CreateTenantForm {
  name: string;
  subdomain?: string;
  contact_email?: string;
  plan_type: 'free' | 'basic' | 'pro' | 'enterprise';
}

export interface CreateStorefrontForm {
  store_name: string;
  store_description?: string;
  contact_email?: string;
}

// Navigation types
export interface NavigationItem {
  name: string;
  href: string;
  icon: React.ComponentType<React.SVGProps<SVGSVGElement>>;
  current: boolean;
}

// Chart data types
export interface ChartData {
  name: string;
  value: number;
  color?: string;
}

export interface TimeSeriesData {
  date: string;
  value: number;
}

// Notification types
export interface Notification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message: string;
  timestamp: string;
  read: boolean;
}

// Zustand store types
export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  setAuthData: (user: User, token: string) => void;
  logout: () => void;
  updateUser: (user: User) => void;
}

export interface UIState {
  sidebarOpen: boolean;
  theme: 'light' | 'dark';
  toggleSidebar: () => void;
  setTheme: (theme: 'light' | 'dark') => void;
}

export interface NotificationState {
  notifications: Notification[];
  addNotification: (notification: Omit<Notification, 'id' | 'timestamp'>) => void;
  removeNotification: (id: string) => void;
  markAsRead: (id: string) => void;
  clearAll: () => void;
} 